from sqlalchemy import false
import streamlit as st
import pandas as pd
import os
# class Data_Split(object):

#     def __init__(self,data):
#         self.data = data

#     def split(data):
#         uploaded_file = data
#         if uploaded_file is not None:        
#             colum = ["Start","End",
#                      "UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B","UPPER_BUS_PHASE_C",
#                     "LOWER_BUS_PHASE_A","LOWER_BUS_PHASE_B","LOWER_BUS_PHASE_C",
#                     "OUTGOING_PHASE_A","OUTGOING_PHASE_B","OUTGOING_PHASE_C",
#                     "UPPER_BUS_PD", "LOWER_BUS_PD", "SPOUT_PD", "OUTGOING_PD"]
        
#             columnA16 = ["Start","End",
#                          "UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B","UPPER_BUS_PHASE_C",
#                          "UPPER_BUS_PD","LOWER_BUS_PD","SPOUT_PD",
#                          ]
                
#             for sheet_name, df1 in pd.read_excel(uploaded_file, index_col=False, sheet_name=None, keep_default_na=False).items():
#                 if sheet_name != 'PD PI tag list' and sheet_name != 'Temp PI tag list':
#                     if sheet_name == 'A16':
                        
#                         # st.table(df1)
#                         df1=df1.iloc[17:]
#                         # st.write(sheet_name)
#                         df1.reset_index(drop=True, inplace=True)
#                         # st.table(df1)
#                         df1.to_csv(f'Temp/{sheet_name}.csv', header=columnA16,encoding='utf-8')
                        
#                     elif  sheet_name == 'A15':
#                         df1=df1.iloc[18:]
#                         # df1=df1.drop(df1.loc[0:16].index, inplace=True)
#                         # st.write(sheet_name)
#                         df1.reset_index(drop=True, inplace=True)
#                         # st.table(df1)
#                         df1.to_csv(f'Temp/{sheet_name}.csv', header=colum, encoding='utf-8')

#                     else:
#                         if sheet_name == 'A1' and len(df1.columns) == 16 :
#                             df1=df1.iloc[: , :-1]
#                         df1=df1.iloc[17:]
#                         # df1=df1.drop(df1.loc[0:16].index, inplace=True)
#                         # st.write(sheet_name)
#                         df1.reset_index(drop=True, inplace=True)
#                         # st.table(df1)
#                         df1.to_csv(f'Temp/{sheet_name}.csv', header=colum, encoding='utf-8')


import streamlit as st
import pandas as pd
import os


class Data_Split(object):

    def __init__(self, data):
        self.data = data

    def split(
        self,
        target_folder="Temp",
        status=None,
        progress_text=None,   # ← ใช้แค่ระดับไฟล์
        progress_bar=None
    ):

        uploaded_file = self.data

        if uploaded_file is None:
            raise ValueError("No file provided")

        os.makedirs(target_folder, exist_ok=True)

        uploaded_file.seek(0)

        sheets = pd.read_excel(
            uploaded_file,
            index_col=False,
            sheet_name=None,
            keep_default_na=False
        )

        ignore = ['PD PI tag list', 'Temp PI tag list']
        valid_sheets = [s for s in sheets if s not in ignore]

        if len(valid_sheets) == 0:
            raise ValueError("No valid sheets")

        success = 0

        # ===== COLUMN DEFINITIONS =====
        colum = [
            "Start","End",
            "UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B","UPPER_BUS_PHASE_C",
            "LOWER_BUS_PHASE_A","LOWER_BUS_PHASE_B","LOWER_BUS_PHASE_C",
            "OUTGOING_PHASE_A","OUTGOING_PHASE_B","OUTGOING_PHASE_C",
            "UPPER_BUS_PD","LOWER_BUS_PD","SPOUT_PD","OUTGOING_PD"
        ]

        columnA16 = [
            "Start","End",
            "UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B","UPPER_BUS_PHASE_C",
            "UPPER_BUS_PD","LOWER_BUS_PD","SPOUT_PD"
        ]

        # ===== PROCESS ALL SHEETS (NO UI UPDATE HERE) =====
        for sheet_name in valid_sheets:

            df1 = sheets[sheet_name]

            try:

                if sheet_name == 'A16':
                    df1 = df1.iloc[17:]
                    df1.reset_index(drop=True, inplace=True)
                    df1.to_csv(f'{target_folder}/{sheet_name}.csv',
                               header=columnA16,
                               encoding='utf-8',
                               index=False)

                elif sheet_name == 'A15':
                    df1 = df1.iloc[18:]
                    df1.reset_index(drop=True, inplace=True)
                    df1.to_csv(f'{target_folder}/{sheet_name}.csv',
                               header=colum,
                               encoding='utf-8',
                               index=False)

                else:
                    if sheet_name == 'A1' and len(df1.columns) == 16:
                        df1 = df1.iloc[:, :-1]

                    df1 = df1.iloc[17:]
                    df1.reset_index(drop=True, inplace=True)
                    df1.to_csv(f'{target_folder}/{sheet_name}.csv',
                               header=colum,
                               encoding='utf-8',
                               index=False)

                success += 1

            except Exception:
                pass

        # ===== FINAL RESULT ONLY =====
        if success == 0:
            raise ValueError("No sheets processed")

        return success, len(valid_sheets)