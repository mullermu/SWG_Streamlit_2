

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression



class SwitchgearFeatureEngineering:

    def __init__(self, df):
        self.df = df.copy()

    # -------------------------------------------------
    # STEP 1 : hourly PD features
    # -------------------------------------------------
    def pd_feature_engineering(self, df):

        df = df.copy()

        pd_cols = [
            "UPPER_BUS_PD",
            "LOWER_BUS_PD",
            "SPOUT_PD",
            "OUTGOING_PD"
        ]

        temp_cols = [
            'UPPER_BUS_PHASE_A','UPPER_BUS_PHASE_B','UPPER_BUS_PHASE_C',
            'LOWER_BUS_PHASE_A','LOWER_BUS_PHASE_B','LOWER_BUS_PHASE_C',
            'OUTGOING_PHASE_A','OUTGOING_PHASE_B','OUTGOING_PHASE_C'
        ]

        pd_cols = [c for c in pd_cols if c in df.columns]

        # datetime
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        df = (
            df.sort_values("datetime")
            .drop_duplicates("datetime")
            .set_index("datetime")
        )

        # continuous hourly index
        full_index = pd.date_range(
            df.index.min(),
            df.index.max(),
            freq="h"
        )

        df = df.reindex(full_index)

        df[pd_cols] = df[pd_cols].interpolate(
            method="time",
            limit=6
        )

        # -------------------------
        # base PD features
        # -------------------------
        df["PD_raw_max"] = df[pd_cols].max(axis=1)

        if len(temp_cols) > 0:
            df["Temp_raw_max"] = df[temp_cols].max(axis=1)

        df["PD_sensor_std"] = df[pd_cols].std(axis=1)

        df["PD_imbalance"] = (
            df[pd_cols].max(axis=1)
            - df[pd_cols].min(axis=1)
        )

        # trend
        df["PD_trend_max"] = (
            df["PD_raw_max"]
            .rolling(24, min_periods=12)
            .median()
        )

        # volatility
        df["PD_volatility"] = (
            df["PD_raw_max"]
            .rolling(24, min_periods=12)
            .std()
        )

        rolling_mean = df["PD_raw_max"].rolling(24, min_periods=12).mean()
        rolling_std = df["PD_raw_max"].rolling(24, min_periods=12).std()

        # spike
        df["PD_spike_max"] = (
            df["PD_raw_max"] - rolling_mean
        ) / (rolling_std + 1e-6)

        # growth
        df["PD_growth_rate"] = (
            df["PD_raw_max"] - rolling_mean
        )

        # slope
        df["PD_slope_24h"] = (
            df["PD_raw_max"]
            - df["PD_raw_max"].shift(24)
        ) / 24

        # persistence
        df["PD_persistence_24h"] = (
            (df["PD_raw_max"] > rolling_mean)
            .rolling(24, min_periods=12)
            .sum()
        )

        # burst
        threshold = (
            df["PD_raw_max"]
            .rolling(24, min_periods=12)
            .quantile(0.95)
        )

        df["PD_burst"] = df["PD_raw_max"] > threshold

        df["PD_burst_count_24h"] = (
            df["PD_burst"]
            .rolling(24, min_periods=12)
            .sum()
        )

        # propagation
        df["PD_spread_count"] = (
            (df[pd_cols] > threshold.values.reshape(-1,1))
            .sum(axis=1)
        )
        # df["PD_spread_count"] = (
        #     df[pd_cols].gt(threshold, axis=0)
        # ).sum(axis=1)

        df["PD_multi_high"] = df["PD_spread_count"] >= 2

        df = df.reset_index().rename(columns={"index":"datetime"})

        return df


    # -------------------------------------------------
    # STEP 2 : daily aggregation
    # -------------------------------------------------
    def group_data_by_daily(self, df):

        df = df.copy()

        df["date"] = pd.to_datetime(df["datetime"]).dt.date

        agg_dict = {}

        pd_features = [
            "PD_raw_max",
            "PD_trend_max",
            "PD_volatility",
            "PD_growth_rate",
            "PD_spike_max",
            "PD_slope_24h",
            "PD_persistence_24h",
            "PD_burst_count_24h",
            "PD_spread_count",
            "Temp_raw_max"
        ]

        for col in pd_features:

            if col in df.columns:

                agg_dict[f"{col}_avg"] = (col,"mean")
                agg_dict[f"{col}_max"] = (col,"max")

        if "PD_multi_high" in df.columns:
            agg_dict["PD_multi_high_count"] = ("PD_multi_high","sum")

        phase_cols = [
            "UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B","UPPER_BUS_PHASE_C",
            "LOWER_BUS_PHASE_A","LOWER_BUS_PHASE_B","LOWER_BUS_PHASE_C",
            "OUTGOING_PHASE_A","OUTGOING_PHASE_B","OUTGOING_PHASE_C"
        ]

        phase_cols = [c for c in phase_cols if c in df.columns]

        if len(phase_cols) > 0:

            df["Temp_system_imbalance"] = (
                df[phase_cols].max(axis=1)
                - df[phase_cols].min(axis=1)
            )

            agg_dict["Temp_system_imbalance_max"] = (
                "Temp_system_imbalance","max"
            )

        daily = (
            df
            .groupby("date")
            .agg(**agg_dict)
            .reset_index()
        )

        return daily


    # -------------------------------------------------
    # STEP 3 : switchgear time-series features
    # -------------------------------------------------
    def generate_switchgear_features(self, df):

        df = df.copy()

        window = 7

        df = df.sort_values("date")

        df["date_diff"] = pd.to_datetime(df["date"]).diff().dt.days

        df["group"] = (df["date_diff"] > 1).cumsum()

        # PD instability
        df["PD_instability"] = (

            df.groupby("group")["PD_trend_max_avg"]
            .rolling(window, min_periods=window)
            .std()
            .reset_index(level=0,drop=True)
        )

        # PD escalation
        df["PD_escalation"] = (

            df["PD_raw_max_avg"]
            -
            df.groupby("group")["PD_raw_max_avg"]
            .rolling(window, min_periods=window)
            .mean()
            .reset_index(level=0,drop=True)
        )

        # slope
        df["PD_slope7"] = (

            df["PD_raw_max_avg"]
            - df["PD_raw_max_avg"].shift(7)

        ) / 7

        # thermal volatility
        if "Temp_system_imbalance_max" in df.columns:

            df["Temp_system_volatility"] = (

                df.groupby("group")["Temp_system_imbalance_max"]
                .rolling(window, min_periods=window)
                .std()
                .reset_index(level=0,drop=True)
            )

        return df


    # -------------------------------------------------
    # PIPELINE
    # -------------------------------------------------
    def run(self):

        # step 1
        hourly = self.pd_feature_engineering(self.df)

        # step 2
        daily = self.group_data_by_daily(hourly)

        # step 3
        features = self.generate_switchgear_features(daily)

        features = features.sort_values("date")

        return hourly, daily, features
