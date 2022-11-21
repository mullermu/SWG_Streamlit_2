from sqlalchemy import false
import streamlit as st
import pandas as pd

class Data_Split(object):

    def __init__(self,data):
        self.data = data

    def split(data):
        uploaded_file = data
        if uploaded_file is not None:        
            colum = ["Start","End","UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B"
                ,"UPPER_BUS_PHASE_C","LOWER_BUS_PHASE_A"
                ,"LOWER_BUS_PHASE_B","LOWER_BUS_PHASE_C"
                ,"OUTGOING_PHASE_A","OUTGOING_PHASE_B"
                ,"OUTGOING_PHASE_C","UPPER_BUS_PD"
                ,"LOWER_BUS_PD","SPOUT_PD","OUTGOING_PD"]
        
            columnA16 = ["Start","End","UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B"
                ,"UPPER_BUS_PHASE_C","UPPER_BUS_PD"
                ,"LOWER_BUS_PD","SPOUT_PD"]
                
            for sheet_name, df1 in pd.read_excel(uploaded_file, index_col=False, sheet_name=None, keep_default_na=False).items():
                if sheet_name != 'PD PI tag list' and sheet_name != 'Temp PI tag list':
                    if sheet_name == 'A16':
                        
                        # st.table(df1)
                        df1=df1.iloc[17:]
                        # st.write(sheet_name)
                        df1.reset_index(drop=True, inplace=True)
                        # st.table(df1)
                        df1.to_csv(f'Temp/{sheet_name}.csv', header=columnA16,encoding='utf-8')
                        
                    elif  sheet_name == 'A15':
                        df1=df1.iloc[18:]
                        # df1=df1.drop(df1.loc[0:16].index, inplace=True)
                        # st.write(sheet_name)
                        df1.reset_index(drop=True, inplace=True)
                        # st.table(df1)
                        df1.to_csv(f'Temp/{sheet_name}.csv', header=colum, encoding='utf-8')

                    else:
                        
                        df1=df1.iloc[17:]
                        # df1=df1.drop(df1.loc[0:16].index, inplace=True)
                        # st.write(sheet_name)
                        df1.reset_index(drop=True, inplace=True)
                        # st.table(df1)
                        df1.to_csv(f'Temp/{sheet_name}.csv', header=colum, encoding='utf-8')