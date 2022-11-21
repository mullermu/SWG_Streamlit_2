import streamlit as st 
from time import sleep
import pandas as pd
import plotly.express as px

class mc_graph(object):
    def get_mc_graph():
        st.header("History Chart")
        selected_mc = st.selectbox('Select Machine History Status', options = pd.read_csv("MC lists/MC_lists.csv"))
            
        path_sheet  = f"output/Predicted Results/{selected_mc}.csv"
        if selected_mc != 'A16':
            mcData=pd.read_csv(path_sheet)
        else:
            # df=pd.read_csv(path_sheet, index_col=0)
            mcData = [1,1]

        def history_chart():
        
            with st.container():
                fig = px.line(mcData, x='Start', y="Status", title=selected_mc)
                st.plotly_chart(fig)



        def details_chart():
            colum = pd.read_csv(f"output/Predicted Results/{selected_mc}.csv").columns.drop(['Start', 'End'])
            selected_details = st.selectbox('Select Parameter Values', options = colum)
            
            with st.container():
                fig = px.line(mcData, x='Start', y=selected_details, title=selected_mc)
                st.plotly_chart(fig)
        history_chart()
        details_chart()
