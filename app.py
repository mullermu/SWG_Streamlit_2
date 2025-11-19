# pip install streamlit
# pip install numpy
# pip install joblib
# pip install openpyxl



# from tkinter import X
import streamlit as st
import pandas as pd
import os
import pandas as pd
import MC_status
import MC_Graph
import model_predict
import glob
import openpyxl 
import openpyxl
import csv

from azure_auth import (
    AuthConfigurationError,
    AzureAuthManager,
    load_auth_config,
)
# from streamlitapp.Data_Input import data_input

st.set_page_config(
    page_title="Swtich Gear Prediction Main Page",
    layout="wide"
)


def ensure_authenticated():
    """Gate the application behind Azure AD authentication."""

    try:
        auth_config = load_auth_config()
    except AuthConfigurationError as exc:
        st.error(
            "Azure AD configuration is missing. Set AZURE_CLIENT_ID, "
            "AZURE_TENANT_ID, AZURE_CLIENT_SECRET, and AZURE_REDIRECT_URI.\n"
            f"Details: {exc}"
        )
        st.stop()

    auth_manager = AzureAuthManager(auth_config)

    query_params_obj = st.query_params
    query_params = dict(query_params_obj)

    def clear_query_params():
        st.query_params.clear()
    auth_flow = st.session_state.get("auth_flow")

    if "code" in query_params and auth_flow:
        result = auth_manager.exchange_code_for_token(dict(query_params), auth_flow)
        if "error" in result:
            st.error(f"Authentication failed: {result.get('error_description')}")
            st.stop()

        st.session_state["user"] = result.get("id_token_claims", {})
        st.session_state.pop("auth_flow", None)
        st.session_state.pop("login_url", None)
        clear_query_params()

    if "user" not in st.session_state:
        st.info(
            "Sign in with your Microsoft work account to continue. "
            "The app requests the User.Read permission."
        )
        if st.button("Sign in with Microsoft", type="primary"):
            st.session_state["auth_flow"] = auth_manager.build_auth_code_flow()
            st.session_state["login_url"] = st.session_state["auth_flow"].get("auth_uri")

        login_url = st.session_state.get("login_url")
        if login_url:
            st.markdown(f"[Continue to Microsoft login]({login_url})")
        st.stop()

    user = st.session_state.get("user", {})
    user_display = user.get("name") or user.get("preferred_username") or "user"
    st.sidebar.success(f"Signed in as {user_display}")
def get_csv(df):
    
    csv = df.to_csv(index=False)
    
    return csv
def get_data1(dtfile):
    dtfile.to_csv (r'Temp/temp.csv', index = False, header=True)

def form_callback():
    st.write(st.session_state.my_option)
    st.write(st.session_state.my_checkbox)

def listmodel(path):
    # return os.urllib(path)
    
    return os.listdir(path)

def listmachine(path):
    return os.listdir(path)


def st_header(data):
    st.title("Switch Gear Status Classification App")
    
    with st.container():
@@ -244,50 +302,51 @@ def simulation_app():

        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()
    # df = input_df.iloc[:]
    # Displays the user input features
    st.subheader('User Input features')

    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(input_df.iloc[:1])
    
    if input_df is not None:
        # Reads in saved classification model
        lstmodel = listmodel('model/')
        # st.write(lstmodel)
        tmp = [i.split('.')[0] for i in lstmodel]
        col1, col2, col3 = st.columns([1,5,1])
        with col2 :
            option = st.selectbox('Select Model:',tmp)
            st.write('You selected model: {}'.format(str(option)))
            lstmodel[tmp.index(option)]
        st_result(lstmodel[tmp.index(option)], input_df, True)
    

def main():
    with st.sidebar:  
    ensure_authenticated()
    with st.sidebar:
            data = None
            data = st_header(data)
            clf = st_body()
            if clf is not None and data is True:
                df = None
                st_result(clf, df, False)
            else:
                st.write('Please upload files and select predection model!')
                
            
            

    tab1, tab2, tab3 = st.tabs(["Summary", "Details", "Simulation"])
    with tab1:
        st.header("Summary")
        status_body() 
        summary_chart()
    with tab2:
        history_chart()
    with tab3:
        simulation_app()
    

main()
