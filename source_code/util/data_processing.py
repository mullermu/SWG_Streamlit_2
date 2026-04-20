"""
Switchgear Data Processing and Dataset Preparation
--------------------------------------------------

This module prepares raw switchgear datasets for machine learning models.
It standardizes raw Excel files, extracts sensor signals, creates time features,
and saves cleaned datasets for prediction pipelines.
"""

import pandas as pd
import numpy as np
import os


# =========================================================
# Processing Class
# =========================================================
class processing:

    def __init__(self, df):
        self.df = df

    # -------------------------------------------------
    # Normalize columns
    # -------------------------------------------------
    def normalize_switchgear_df(self):

        df = self.df.copy()

        target_cols = [
            "Start", "End",
            "UPPER_BUS_PHASE_A", "UPPER_BUS_PHASE_B", "UPPER_BUS_PHASE_C",
            "LOWER_BUS_PHASE_A", "LOWER_BUS_PHASE_B", "LOWER_BUS_PHASE_C",
            "OUTGOING_PHASE_A", "OUTGOING_PHASE_B", "OUTGOING_PHASE_C",
            "UPPER_BUS_PD", "LOWER_BUS_PD", "SPOUT_PD", "OUTGOING_PD",
            "POWER", "VOLTAGE", "FREQUENCY"
        ]

        df_out = pd.DataFrame(index=df.index)

        # ensure all columns exist
        for col in target_cols:
            if col in df.columns:
                df_out[col] = df[col]
            else:
                df_out[col] = np.nan

        # datetime features
        df_out["datetime"] = pd.to_datetime(df_out["Start"], errors="coerce")
        df_out["date"] = df_out["datetime"].dt.date
        df_out["year"] = df_out["datetime"].dt.year

        return df_out

    # -------------------------------------------------
    # Add additional time columns
    # -------------------------------------------------
    def addcolumns_date(self, df, col_date="datetime"):

        df = df.copy()

        df["month"] = df[col_date].dt.month
        df["day"] = df[col_date].dt.day
        df["date"] = df[col_date].dt.date
        df["Q"] = df[col_date].dt.quarter

        return df

    # -------------------------------------------------
    # Run full pipeline
    # -------------------------------------------------
    def run(self):

        df_out = self.normalize_switchgear_df()
        df_out = self.addcolumns_date(df_out, col_date="datetime")

        return df_out





class split_and_savefile:

    def __init__(self, data):
        self.data = data

    def split(
        self,
        target_folder="data/raw_data",
        status=None,
        progress_text=None,
        progress_bar=None
    ):

        uploaded_file = self.data

        if uploaded_file is None:
            if status:
                status.write("❌ No file provided")
            return

        # ------------------------------------
        # Create folder
        # ------------------------------------
        os.makedirs(target_folder, exist_ok=True)

        # ------------------------------------
        # Read Excel
        # ------------------------------------
        xls = pd.ExcelFile(uploaded_file)
        sheets = xls.sheet_names

        ignore_sheets = [
            "Temp PI tag list",
            "PD PI tag list"
        ]

        target_cols = [
            "Start", "End",
            "UPPER_BUS_PHASE_A", "UPPER_BUS_PHASE_B", "UPPER_BUS_PHASE_C",
            "LOWER_BUS_PHASE_A", "LOWER_BUS_PHASE_B", "LOWER_BUS_PHASE_C",
            "OUTGOING_PHASE_A", "OUTGOING_PHASE_B", "OUTGOING_PHASE_C",
            "UPPER_BUS_PD", "LOWER_BUS_PD", "SPOUT_PD", "OUTGOING_PD",
            "POWER", "VOLTAGE", "FREQUENCY"
        ]

        success = []
        failed = []

        # ------------------------------------
        # Valid sheets
        # ------------------------------------
        valid_sheets = [s for s in sheets if s not in ignore_sheets]
        total = len(valid_sheets)

        if total == 0:
            raise ValueError("❌ No valid sheets found")

        # ------------------------------------
        # Process sheets
        # ------------------------------------
        for i, sheet in enumerate(valid_sheets, start=1):

            # UPDATE LINE (not append)
            if progress_text:
                progress_text.markdown(
                    f"📄 **[{i}/{total}] Processing sheet: {sheet}**"
                )

            # UPDATE PROGRESS BAR
            if progress_bar:
                progress_bar.progress(i / total)

            try:

                # IMPORTANT for Streamlit uploader
                uploaded_file.seek(0)

                df_raw = pd.read_excel(
                    uploaded_file,
                    sheet_name=sheet,
                    header=None
                )

                # Header location
                header_row = 19 if sheet == "A15" else 18
                data_row = header_row + 1

                df = df_raw.iloc[data_row:].reset_index(drop=True)

                # Assign column names
                df.columns = target_cols

                # Run processing pipeline
                df1 = processing(df).run()

                # Drop empty rows
                df1 = df1.dropna(subset=target_cols, how="all")

                # Save CSV
                save_path = os.path.join(target_folder, f"{sheet}.csv")
                df1.to_csv(save_path, index=False)

                success.append(sheet)

            except Exception as e:

                failed.append(sheet)

                # if status:
                #     status.write(f"❌ {sheet} failed: {e}")

        # ------------------------------------
        # Summary (single message)
        # ------------------------------------
        if progress_text:
            progress_text.markdown(
                f"**Done: {len(success)}/{total} sheets processed**"
            )

        if status:
            status.write(
                f"SUCCESS: {len(success)} | FAILED: {len(failed)}"
            )

        # ------------------------------------
        # Validation
        # ------------------------------------
        if len(success) == 0:
            raise ValueError("❌ No valid sheets processed")

        if len(failed) > 5:
            raise ValueError(f"❌ Too many failed sheets: {failed}")

def prepare_switchgear_df(df):

    import pandas as pd
    import numpy as np

    df = df.copy()

    # -------------------------
    # Convert datetime
    # -------------------------
    for col in ['Start','End']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # create datetime
    if "datetime" not in df.columns and "Start" in df.columns:
        df["datetime"] = pd.to_datetime(df["Start"], errors="coerce")

    if "date" not in df.columns:
        df["date"] = pd.to_datetime(df["datetime"], errors="coerce").dt.date

    # -------------------------
    # Numeric columns
    # -------------------------
    numeric_cols = [
        'UPPER_BUS_PHASE_A', 'UPPER_BUS_PHASE_B', 'UPPER_BUS_PHASE_C',
        'LOWER_BUS_PHASE_A', 'LOWER_BUS_PHASE_B', 'LOWER_BUS_PHASE_C',
        'OUTGOING_PHASE_A', 'OUTGOING_PHASE_B', 'OUTGOING_PHASE_C',
        'UPPER_BUS_PD', 'LOWER_BUS_PD', 'SPOUT_PD', 'OUTGOING_PD',
        'POWER', 'VOLTAGE', 'FREQUENCY'
    ]

    existing_cols = [c for c in numeric_cols if c in df.columns]

    for col in existing_cols:

        df[col] = (
            df[col]
            .replace([' ', '', 'NA', 'None'], np.nan)  # clean string
        )

        df[col] = pd.to_numeric(
            df[col],
            errors='coerce'
        ).astype('float32')

    return df
