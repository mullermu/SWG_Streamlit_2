"""
Neon Postgres persistence for Switchgear Health Index results
---------------------------------------------------------------
"""

import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert

ENV_DATABASE_URL = "DATABASE_URL"

TABLE_NAME = "switchgear_results"

BOOLEAN_COLUMNS = {"pd_burst", "pd_multi_high"}
TIMESTAMP_COLUMNS = {"datetime", "start", "end"}
DATE_COLUMNS = {"date"}

FEATURE_COLUMNS = [
    "upper_bus_phase_a", "upper_bus_phase_b", "upper_bus_phase_c",
    "lower_bus_phase_a", "lower_bus_phase_b", "lower_bus_phase_c",
    "outgoing_phase_a", "outgoing_phase_b", "outgoing_phase_c",
    "upper_bus_pd", "lower_bus_pd", "spout_pd", "outgoing_pd",
    "power", "voltage", "frequency",
    "year", "month", "day", "q",
    "pd_raw_max", "temp_raw_max", "pd_sensor_std", "pd_imbalance",
    "pd_trend_max", "pd_volatility", "pd_spike_max", "pd_growth_rate",
    "pd_slope_24h", "pd_persistence_24h", "pd_burst",
    "pd_burst_count_24h", "pd_spread_count", "pd_multi_high",
]

CONFLICT_KEY = ["machine", "datetime"]


def _get_setting(env_var: str) -> str:
    """Read a configuration value from an env var or Streamlit secrets."""

    env_value = (os.getenv(env_var) or "").strip()
    if env_value:
        return env_value

    try:
        secrets = st.secrets
    except (RuntimeError, AttributeError):
        secrets = {}

    value = str(secrets.get(env_var, "")).strip()

    return value


@st.cache_resource
def get_engine():
    connection_string = _get_setting(ENV_DATABASE_URL)

    if not connection_string:
        raise RuntimeError(
            "DATABASE_URL is not configured. Set it as an environment variable "
            "or add it to .streamlit/secrets.toml (see .streamlit/secrets.toml.example)."
        )

    return create_engine(connection_string, pool_pre_ping=True)


def _column_ddl():
    columns = ['machine TEXT NOT NULL']

    for col in sorted(TIMESTAMP_COLUMNS):
        name = f'"{col}"' if col == "end" else col
        columns.append(f"{name} TIMESTAMP")

    for col in DATE_COLUMNS:
        columns.append(f"{col} DATE")

    for col in FEATURE_COLUMNS:
        col_type = "BOOLEAN" if col in BOOLEAN_COLUMNS else "DOUBLE PRECISION"
        columns.append(f"{col} {col_type}")

    columns.append("health_index DOUBLE PRECISION")
    columns.append("status INTEGER")
    columns.append("UNIQUE (machine, datetime)")

    return ",\n    ".join(columns)


def ensure_table_exists(engine):
    ddl = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        {_column_ddl()}
    );
    CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_machine ON {TABLE_NAME} (machine);
    """

    with engine.begin() as conn:
        conn.execute(text(ddl))


def _prepare_dataframe(df: pd.DataFrame, machine: str) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    df["machine"] = machine

    for col in TIMESTAMP_COLUMNS | DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    known_columns = (
        ["machine"]
        + sorted(TIMESTAMP_COLUMNS)
        + list(DATE_COLUMNS)
        + FEATURE_COLUMNS
        + ["health_index", "status"]
    )
    keep_columns = [c for c in known_columns if c in df.columns]
    result = df[keep_columns]

    # Cast to object first: assigning None into a float/datetime64 dtype
    # column gets silently re-coerced back to NaN/NaT by numpy, which
    # Postgres would store as literal NaN instead of NULL.
    return result.astype(object).where(pd.notnull(result), None)


def upsert_dataframe(engine, df: pd.DataFrame, machine: str, chunk_size: int = 500) -> int:
    df = _prepare_dataframe(df, machine)

    if df.empty:
        return 0

    table_columns = list(df.columns)
    rows = df.to_dict(orient="records")

    metadata = MetaData()
    table = Table(TABLE_NAME, metadata, autoload_with=engine)

    with engine.begin() as conn:
        for start in range(0, len(rows), chunk_size):
            chunk = rows[start:start + chunk_size]
            stmt = pg_insert(table).values(chunk)
            stmt = stmt.on_conflict_do_update(
                index_elements=CONFLICT_KEY,
                set_={c: getattr(stmt.excluded, c) for c in table_columns if c not in CONFLICT_KEY},
            )
            conn.execute(stmt)

    return len(rows)


def reset_table(engine):
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME}"))


def fetch_all_results(engine) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM {TABLE_NAME} ORDER BY machine, datetime", engine)
