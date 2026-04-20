"""
Switchgear Prediction Module
----------------------------

This module performs anomaly detection using a trained LSTM Autoencoder
model. It loads the trained model bundle and applies it to the engineered
switchgear feature dataset to calculate anomaly scores and health indices.

The prediction pipeline transforms time-series features into sequences,
reconstructs them using the autoencoder model, and evaluates reconstruction
error to determine equipment health condition.
"""


# ===============================
# Load model class
# ===============================

import joblib
import json
from keras.models import load_model
import tensorflow as tf
import pandas as pd
import numpy as np

import streamlit as st


@st.cache_resource
def load_model_bundle(
    path="model_bundle_switchgear",
    model_name="lstm_autoencoder_switchgear.keras"
):

    # load model
    model = load_model(f"{path}/{model_name}")

    # load scaler
    scaler = joblib.load(f"{path}/scaler.pkl")

    # load config
    config = joblib.load(f"{path}/config.pkl")

    # load health index meta
    with open(f"{path}/health_index_meta.json", "r") as f:
        meta = json.load(f)

    print("✅ Model bundle loaded")

    return model, scaler, config, meta
def detect_anomaly(
    df,
    feature_names,
    scaler,
    model,
    threshold,
    window_size=7
):

    import numpy as np
    import pandas as pd

    # -------------------------
    # sort time
    # -------------------------
    df = df.sort_values("date").reset_index(drop=True)

    # -------------------------
    # select feature
    # -------------------------
    df_feat = df[["date"] + feature_names].copy()

    # drop rows with NaN
    df_feat = df_feat.dropna(subset=feature_names).reset_index(drop=True)

    if len(df_feat) <= window_size:
        raise ValueError("Data length must be greater than window_size")

    # -------------------------
    # scaling
    # -------------------------
    X = df_feat[feature_names]
    X_scaled = scaler.transform(X)

    # -------------------------
    # create sequence
    # -------------------------
    X_seq = np.array([
        X_scaled[i:i + window_size]
        for i in range(len(X_scaled) - window_size + 1)
    ])

    # -------------------------
    # reconstruction
    # -------------------------
    recon = model.predict(X_seq, verbose=0)

    # -------------------------
    # reconstruction error
    # -------------------------
    error = np.mean(
        (X_seq - recon) ** 2,
        axis=(1, 2)
    )

    # -------------------------
    # align output dataframe
    # -------------------------
    df_out = df_feat.iloc[window_size-1:].copy()

    df_out["anomaly_score"] = error
    df_out["anomaly"] = df_out["anomaly_score"] > threshold

    # -------------------------
    # persistence rule
    # -------------------------
    df_out["anomaly_persist"] = (
        df_out["anomaly"]
        .rolling(3, min_periods=1)
        .sum()
    )

    df_out["alarm"] = df_out["anomaly_persist"] >= 2

    return df_out

def daily_risk(df):

    df["date"] = df["datetime"].dt.date

    daily = df.groupby("date").agg({

        "anomaly_score":"max",
        "PD_raw_max_max": "max",
        "Temp_raw_max_max": "max"

    }).reset_index()

    return daily
def risk_7day(daily):

    daily["risk_7day"] = (
        daily["anomaly_score"]
        .rolling(7, min_periods=7)
        .max()
    )

    return daily
def classify_risk(df, q1, q2):

    df = df.copy()

    conditions = [
        df["anomaly_score"] < q1,
        df["anomaly_score"] < q2
    ]

    choices = ["LOW", "MEDIUM"]

    df["risk_level"] = np.select(
        conditions,
        choices,
        default="HIGH"
    )

    return df

import numpy as np

def classify_risk2(df):

    df = df.copy()

    # -------------------------
    # handle missing values
    # -------------------------
    df["PD_raw_max_max"] = df["PD_raw_max_max"].fillna(0)
    df["Temp_raw_max_max"] = df["Temp_raw_max_max"].fillna(0)
    df["anomaly_score"] = df["anomaly_score"].fillna(0)

    # -------------------------
    # strong sensor condition
    # -------------------------
    sensor_high = (
        (df["PD_raw_max_max"] >= 1000) |
        (df["Temp_raw_max_max"] >= 60)
    )

    # rule 1 : health 1 + strong sensor → 2
    df.loc[
        (df["health_index"] == 1) & sensor_high,
        "health_index"
    ] = 2

    # rule 2 : health 2 + strong sensor → 3
    df.loc[
        (df["health_index"] == 2) & sensor_high,
        "health_index"
    ] = 3

    # -------------------------
    # moderate sensor condition
    # -------------------------
    sensor_high2 = (
        (df["PD_raw_max_max"] >= 700) |
        (df["Temp_raw_max_max"] >= 40)
    )

    # rule 3 : anomaly extreme + moderate sensor → 3
    df.loc[
        (df["health_index"] == 2) &
        (df["anomaly_score"] > 1000) &
        sensor_high2,
        "health_index"
    ] = 3

    # # -------------------------
    # # rule 4 : very extreme PD → 4
    # # -------------------------
    # df.loc[
    #     (df["PD_raw_max_max"] >= 8000) &
    #     (df["anomaly_score"] > 1000) &
    #     sensor_high2,
    #     "health_index"
    # ] = 4

    return df

def prepare_result_dataset(
    df_signal,
    df_risk,
    date_col="date",
    health_col="health_index"
):

    import pandas as pd

    df_signal = df_signal.copy()
    df_risk = df_risk.copy()

    df_signal[date_col] = pd.to_datetime(df_signal[date_col])
    df_risk[date_col] = pd.to_datetime(df_risk[date_col])

    df = pd.merge(
        df_signal,
        df_risk[[date_col, health_col]],
        on=date_col,
        how="left"
    ).sort_values(date_col)

    df[health_col] = df[health_col].ffill().bfill()

    return df