"""
Switchgear Output Processing and Visualization Module
-----------------------------------------------------

This module processes model prediction outputs and generates monitoring
signals and visualization dashboards for switchgear health analysis.

The module combines model prediction results with raw operational data
to create interpretable health indicators and failure warning signals.
It also provides visualization tools used in the Streamlit dashboard.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st



def plot_daily_monitor(
    df: pd.DataFrame,
    date_col: str = "date",
    health_col: str = "health_index",
    pd_col: str = "PD_raw_max",
    temp_col: str = "Temp_raw_max",
    pd_threshold: float = 1000,
    temp_threshold: float = 60,
    ylim: tuple | None = None,
    title: str = "Daily Switchgear Monitoring",
    use_streamlit: bool = True
):


    df = df.copy()

    # -------------------------
    # type conversion
    # -------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    for c in [pd_col, temp_col]:
        if c in df.columns:
            df[c] = (
                df[c]
                .astype(str)
                .str.replace(",", "")
                .pipe(pd.to_numeric, errors="coerce")
            )

    if health_col in df.columns:
        df[health_col] = pd.to_numeric(df[health_col], errors="coerce")

    df = df.sort_values(date_col)

    # -------------------------
    # risk colors
    # -------------------------
    colors = {
        1: "green",
        2: "orange",
        3: "red",
        4: "#5B0000"
    }

    # -------------------------
    # create figure
    # -------------------------
    fig, ax = plt.subplots(figsize=(20, 6))

    # -------------------------
    # background risk blocks
    # -------------------------
    if health_col in df.columns:

        risk_df = df[[date_col, health_col]].drop_duplicates()

        risk_df["block"] = (
            risk_df[health_col] != risk_df[health_col].shift()
        ).cumsum()

        for _, g in risk_df.groupby("block"):

            risk = g[health_col].iloc[0]

            if pd.notna(risk):
                ax.axvspan(
                    g[date_col].min(),
                    g[date_col].max(),
                    color=colors.get(risk, "gray"),
                    alpha=0.12
                )

    # -------------------------
    # plot signals
    # -------------------------
    if pd_col in df.columns:
        ax.plot(
            df[date_col],
            df[pd_col],
            label="PD_max",
            linewidth=2
        )

    # if temp_col in df.columns:
    #     ax.plot(
    #         df[date_col],
    #         df[temp_col],
    #         label="Temp_max",
    #         linewidth=2
    #     )

    # -------------------------
    # thresholds
    # -------------------------
    if pd_threshold is not None:
        ax.axhline(
            pd_threshold,
            linestyle="--",
            color="red",
            alpha=0.7,
            label=f"PD threshold ({pd_threshold})"
        )

    # if temp_threshold is not None:
    #     ax.axhline(
    #         temp_threshold,
    #         linestyle="--",
    #         color="purple",
    #         alpha=0.7,
    #         label=f"Temp threshold ({temp_threshold})"
    #     )

    # -------------------------
    # axis settings
    # -------------------------
    if ylim:
        ax.set_ylim(ylim)

    ax.set_title(title)
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)

    plt.tight_layout()

    # -------------------------
    # render
    # -------------------------
    if use_streamlit:
        st.pyplot(fig)
    else:
        plt.show()

    plt.close(fig)

def plot_signal_with_daily_risk(
    df: pd.DataFrame,
    signal_type: str = "pd",
    date_col: str = "date",
    health_col: str = "health_index",
    ylim: tuple | None = None,
    title: str | None = None,
) -> None:

    df = df.copy()

    # -------------------------
    # column definitions
    # -------------------------
    pd_cols = [
        "UPPER_BUS_PD", "LOWER_BUS_PD", "SPOUT_PD", "OUTGOING_PD"
    ]

    temp_cols = [
        "UPPER_BUS_PHASE_A", "UPPER_BUS_PHASE_B", "UPPER_BUS_PHASE_C",
        "LOWER_BUS_PHASE_A", "LOWER_BUS_PHASE_B", "LOWER_BUS_PHASE_C",
        "OUTGOING_PHASE_A", "OUTGOING_PHASE_B", "OUTGOING_PHASE_C"
    ]

    voltage_cols = ["VOLTAGE"]

    # -------------------------
    # select columns
    # -------------------------
    threshold = None

    if signal_type == "pd":

        cols = [c for c in pd_cols if c in df.columns]

        if not cols and "PD_raw_max_max" in df.columns:
            cols = ["PD_raw_max_max"]

        if title is None:
            title = "PD Signals"

        if ylim is None:
            ylim = (0, 2000)

        threshold = 1000

    elif signal_type == "temp":

        cols = [c for c in temp_cols if c in df.columns]

        if not cols and "Temp_raw_max_max" in df.columns:
            cols = ["Temp_raw_max_max"]

        if title is None:
            title = "Temperature Sensors"

        threshold = 60

    elif signal_type == "voltage":

        cols = [c for c in voltage_cols if c in df.columns]

        if title is None:
            title = "Voltage Sensors"

    else:
        raise ValueError("signal_type must be 'pd', 'temp', or 'voltage'")

    # -------------------------
    # type conversion
    # -------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    signal_cols = pd_cols + temp_cols + voltage_cols + [
        "PD_raw_max_max",
        "Temp_raw_max_max"
    ]

    for c in signal_cols:
        if c in df.columns:

            df[c] = (
                df[c]
                .astype(str)
                .str.replace(",", "")
                .pipe(pd.to_numeric, errors="coerce")
            )

    if health_col in df.columns:
        df[health_col] = pd.to_numeric(df[health_col], errors="coerce")

    df = df.sort_values(date_col)

    # -------------------------
    # risk colors
    # -------------------------
    colors = {
        1: "green",
        2: "orange",
        3: "red",
        4: "#5B0000"
    }

    # -------------------------
    # create figure
    # -------------------------
    fig, ax = plt.subplots(figsize=(20, 5))

    # -------------------------
    # risk blocks
    # -------------------------
    if health_col in df.columns:

        risk_df = df[[date_col, health_col]].drop_duplicates()

        risk_df["block"] = (
            risk_df[health_col] != risk_df[health_col].shift()
        ).cumsum()

        for _, g in risk_df.groupby("block"):

            risk = g[health_col].iloc[0]

            if pd.notna(risk):

                ax.axvspan(
                    g[date_col].min(),
                    g[date_col].max(),
                    color=colors.get(risk, "gray"),
                    alpha=0.12
                )

    # -------------------------
    # plot signals
    # -------------------------
    for c in cols:

        ax.plot(
            df[date_col],
            df[c],
            label=c,
            linewidth=1.5
        )

    # -------------------------
    # threshold line
    # -------------------------
    if threshold is not None:

        ax.axhline(
            threshold,
            color="red",
            linestyle="--",
            alpha=0.7,
            label=f"threshold {threshold}"
        )

    # -------------------------
    # axis settings
    # -------------------------
    if ylim:
        ax.set_ylim(ylim)

    ax.set_title(title)

    ax.legend(loc="upper right")

    ax.grid(alpha=0.3)

    plt.tight_layout()

    # -------------------------
    # streamlit render
    # -------------------------
    st.pyplot(fig)

    plt.close(fig)


    