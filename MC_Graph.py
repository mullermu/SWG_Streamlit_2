import streamlit as st
from time import sleep
import pandas as pd
import plotly.express as px
import openpyxl

def _read_sheet_read_only(path, sheet_name):
    # read_only avoids openpyxl building the full in-memory cell/style graph
    # for every sheet in the workbook just to extract one — Results.xlsx
    # keeps growing via the "save to database" append flow, so a normal-mode
    # pd.read_excel() parse here gets more expensive with every save.
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        ws = wb[sheet_name]
        rows = ws.iter_rows(values_only=True)
        header = next(rows)
        data = list(rows)
    finally:
        wb.close()

    df = pd.DataFrame(data, columns=header)

    # Cells were written from csv.reader() rows (all strings, since the csv
    # module doesn't type-infer), so openpyxl's read_only mode returns them
    # as plain text. pd.read_excel() used to auto-infer numeric dtypes on
    # top of that; replicate it here so charts still get numeric columns
    # instead of strings. Only adopt the numeric version of a column if
    # converting it doesn't turn any additional values into NaN (e.g. this
    # correctly leaves "Start"/"End" datetime-text columns alone).
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.isna().sum() == df[col].isna().sum():
            df[col] = converted

    return df

class mc_graph(object):
    def get_mc_graph():
        st.header("History Chart")
        selected_mc = st.selectbox('Select Machine History Status', options = pd.read_csv("MC lists/MC_lists.csv"))

        path_sheet  = f"output/Predicted Results/{selected_mc}.csv"
        if selected_mc != 'A16':
            mcData = _read_sheet_read_only('output/Predicted Results/Results.xlsx', selected_mc)
            # mcData=pd.read_csv(path_sheet)
        else:
            # df=pd.read_csv(path_sheet, index_col=0)
            mcData = [1,1]

        def history_chart():
        
            with st.container():
                fig = px.line(mcData, x='Start', y="Status", title=selected_mc)
                st.plotly_chart(fig)



        def details_chart():

            colum = mcData.columns.drop(['Start', 'End'])
            selected_details = st.selectbox('Select Parameter Values', options = colum)
            
            with st.container():
                fig = px.line(mcData, x='Start', y=selected_details, title=selected_mc)
                st.plotly_chart(fig)
        history_chart()
        details_chart()
