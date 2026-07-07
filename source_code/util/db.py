"""
Neon Postgres persistence for Switchgear Health Index results
---------------------------------------------------------------
"""

import os
import ssl

import pandas as pd
import streamlit as st
from sqlalchemy import (
    create_engine, Column, Table, MetaData,
    String, DateTime, Date, Float, Boolean, Integer,
    UniqueConstraint, Index, text,
)
from sqlalchemy.engine import make_url
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

# Defined explicitly (not reflected from the DB) so upserts never need an
# extra round-trip to introspect the schema before every insert.
metadata = MetaData()

switchgear_results = Table(
    TABLE_NAME,
    metadata,
    Column("id", Integer, primary_key=True),
    Column("machine", String, nullable=False),
    Column("datetime", DateTime),
    Column("start", DateTime),
    Column("end", DateTime),
    Column("date", Date),
    *[
        Column(col, Boolean if col in BOOLEAN_COLUMNS else Float)
        for col in FEATURE_COLUMNS
    ],
    Column("health_index", Float),
    Column("status", Integer),
    UniqueConstraint("machine", "datetime"),
    Index(f"idx_{TABLE_NAME}_machine", "machine"),
)


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

    # Use pg8000 (a pure-Python driver, no bundled/compiled OpenSSL) instead
    # of psycopg2/psycopg: both are native C extensions that link their own
    # copy of OpenSSL, which conflicts with TensorFlow's own bundled SSL/
    # crypto code (via grpcio) in the same process and causes native heap
    # corruption crashes during the TLS handshake. pg8000 uses Python's
    # stdlib ssl module instead, sidestepping that whole class of bug.
    url = make_url(connection_string).set(drivername="postgresql+pg8000")

    # sslmode/channel_binding are libpq-specific query params pg8000 doesn't
    # understand (and would fail on as unexpected connect() kwargs) — Neon
    # requires SSL, so it's configured explicitly via ssl_context instead.
    url = url.difference_update_query(["sslmode", "channel_binding"])

    return create_engine(
        url,
        pool_pre_ping=True,
        connect_args={
            "ssl_context": ssl.create_default_context(),
            "timeout": 10,
        },
    )


def ensure_table_exists(engine):
    metadata.create_all(engine, checkfirst=True)


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


def upsert_dataframe(conn, df: pd.DataFrame, machine: str, chunk_size: int = 200) -> int:
    """Upsert one machine's dataframe using an already-open connection/transaction."""

    df = _prepare_dataframe(df, machine)

    if df.empty:
        return 0

    table_columns = list(df.columns)
    rows = df.to_dict(orient="records")

    # Built once, without an explicit multi-row .values(...) list: passing a
    # list of param dicts to conn.execute() lets SQLAlchemy's own
    # "insertmanyvalues" batching handle chunking, instead of us hand-building
    # one giant combined VALUES(...),(...),(...) statement per chunk (which is
    # a known trigger for low-level driver/C-extension crashes on large
    # multi-row inserts).
    stmt = pg_insert(switchgear_results)
    stmt = stmt.on_conflict_do_update(
        index_elements=CONFLICT_KEY,
        set_={c: stmt.excluded[c] for c in table_columns if c not in CONFLICT_KEY},
    )

    for start in range(0, len(rows), chunk_size):
        conn.execute(stmt, rows[start:start + chunk_size])

    return len(rows)


def reset_table(engine):
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME}"))


@st.cache_data(ttl=60, show_spinner=False)
def fetch_all_results(_engine) -> pd.DataFrame:
    # Leading underscore tells st.cache_data to key on call identity rather
    # than trying to hash the Engine object; the ttl bounds how stale a
    # repeated "download all" click can be without hitting Postgres again.
    return pd.read_sql(f"SELECT * FROM {TABLE_NAME} ORDER BY machine, datetime", _engine)
