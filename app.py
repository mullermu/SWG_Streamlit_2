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
import csv
# from streamlitapp.Data_Input import data_input

st.set_page_config(
    page_title="Swtich Gear Prediction Main Page",
    layout="wide"
)
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
        
        col1, col2, col3 = st.columns([1,10,1])
        
        with col2 :
            # st.markdown("{}".format(str(word)))
            uploaded_file = st.file_uploader("Choose a A1-A16 file")
            
            # st.markdown("{}".format(str(word)))
            uploaded_file2 = st.file_uploader("Choose a A18-A31 file")
            
            if uploaded_file is not None and uploaded_file2 is not None:
                import data_split
                data_split.Data_Split.split(uploaded_file)
                data_split.Data_Split.split(uploaded_file2)
                data = True
                
                # st.write(data.head())
                
                # get_data1(data)
                # st.table(data)
                # import Data_split
                # Data_split.data_input(data)
    return data



def st_body():
    
    # url = 'https://raw.githubusercontent.com/mullermu/SWG_Streamlit/tree/main/streamlitapp/model/'
    lstmodel = listmodel('model/')
    # st.write(lstmodel)
    tmp = [i.split('.')[0] for i in lstmodel]
    col1, col2, col3 = st.columns([1,10,1])
    with col2 :
        with st.form(key='my_form'):
            option = st.selectbox('Select Model:',tmp,key="my_option")
            submitted = st.form_submit_button('selected model and predict')
            if submitted:
                st.write('You selected model: {}'.format(str(option)))
            return lstmodel[tmp.index(option)]
                
    # import requests
    # from bs4 import BeautifulSoup

    # # URL on the Github where the csv files are stored
    # github_url = 'https://https://github.com/mullermu/SWG_Streamlit_2/tree/master/model'  # change USERNAME, REPOSITORY and FOLDER with actual name

    # result = requests.get(github_url)

    # soup = BeautifulSoup(database.text, 'html.parser')
    # csvfiles = soup.find_all(title=result.compile("\.csv$"))

    # filename = [ ]
    # for i in csvfiles:
    #         filename.append(i.extract().get_text())


def st_result(clf, df, sim = False):
    if clf is not None:
        if sim is not True:  
            df = None
            model_predict.get_predict_result.getResult(clf, df, False)
            download_results()
        else:
            model_predict.get_predict_result.getResult(clf, df, True)
        # model = joblib.load(os.path.join("../model/",clf))
        # z = model.predict(X)
        # res = pd.concat([data,pd.DataFrame(z,columns=['Status'])],axis=1)
        # col1, col2, col3 = st.columns([1,1,1])
        # with col2 :
        #     st.download_button("Download Classification File",get_csv(res),"../output/result_app.csv")
def create_last_results():
    files = [os.path.split(filename) for filename in glob.glob("output/Predicted Results/*.csv")]
    wb = openpyxl.Workbook()
    del wb[wb.sheetnames[0]]        # Remove the default 'Sheet1'
    for f_path, f_name in files:
        (f_short_name, f_extension) = os.path.splitext(f_name)
        with open(os.path.join(f_path, f_name)) as f_input:
            # st.write(f_short_name)
            ws = wb.create_sheet(title=os.path.basename(f_short_name))
            for row in csv.reader(f_input):
                ws.append(row)
    wb.save('output/Predicted Results/Last_Results.xlsx')
def download_results():
        
    files = [os.path.split(filename) for filename in glob.glob("output/Predicted Results/*.csv")]
    st.write("Data Predicted")

    saveToDB = st.radio(
    "Do you want to save data to database?",
    ('Yes, This is new data.', 'No, Data was the same as the old one.','Replace all with the new one.'))
    saveBT = st.button('Save to Database')
    if saveToDB == 'Yes, This is new data.' and saveBT == True:
        wb = openpyxl.load_workbook('output/Predicted Results/Results.xlsx')
        for f_path, f_name in files:
            (f_short_name, f_extension) = os.path.splitext(f_name)
            with open(os.path.join(f_path, f_name)) as f_input:
                ws = wb[f_short_name]
                csv_reader = csv.reader(f_input)
                first_line = next(csv_reader)
                # st.write(first_line)
                for row in csv.reader(f_input):
                    if row != first_line:
                        ws.append(row)
        wb.save('output/Predicted Results/Results.xlsx')
        create_last_results()
        st.write("Added to Database")

    elif saveToDB == 'No, Data was the same as the old one.' and saveBT == True:
        st.write("Nothing saved")
        create_last_results()
    elif saveToDB == 'Replace all with the new one.' and saveBT == True:
        wb = openpyxl.Workbook()
        del wb[wb.sheetnames[0]]        # Remove the default 'Sheet1'
        for f_path, f_name in files:
            (f_short_name, f_extension) = os.path.splitext(f_name)
            with open(os.path.join(f_path, f_name)) as f_input:
                # st.write(f_short_name)
                ws = wb.create_sheet(title=os.path.basename(f_short_name))
                for row in csv.reader(f_input):
                    ws.append(row)
        wb.save('output/Predicted Results/Results.xlsx')
        st.write("Replaced to Database")
        create_last_results()
    
    downloadResults = st.radio(
    "Which file do you would like to download?",
    ('Download last results.', 'Download all database results.'))
    if downloadResults == 'Download last results.':
        my_file = open('output/Predicted Results/Last_Results.xlsx', 'rb')
        fileName = 'Last_Results.xlsx'
    elif downloadResults == 'Download all database results.':
        my_file = open('output/Predicted Results/Results.xlsx', 'rb')
        fileName = 'Database_Results.xlsx'
        
    st.download_button(label = 'Download Results', data = my_file, file_name = fileName, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

def status_body():
    status = MC_status.MC_status.st_status()
    return status

def summary_chart():
    st.header("Summary Chart")
    chart_data = pd.DataFrame(
    MC_status.MC_status.sum_status(),
    columns=['Summary'],
    index=['Stage A', 'Stage B', 'Stage C','Stage D'])
    st.bar_chart(chart_data)

def history_chart():
    MC_Graph.mc_graph.get_mc_graph()

def simulation_app():
    st.write("""
    # Simulation Prediction App
    """)
    def user_input_features():
        
        col1, col2 = st.columns([1,1])
        with col1 :
            from datetime import date
            Start_Time = date.today()
            End_Time = date.today()
            UPPER_BUS_PHASE_A = st.slider('UPPER BUS PHASE A Temperature', 0.00, 100.00, 50.00)
            UPPER_BUS_PHASE_B = st.slider('UPPER BUS PHASE B Temperature', 0.00, 100.00, 50.00)
            UPPER_BUS_PHASE_C = st.slider('UPPER BUS PHASE C Temperature', 0.00, 100.00, 50.00)
            LOWER_BUS_PHASE_A = st.slider('LOWER BUS PHASE A Temperature', 0.00, 100.00, 50.00)
            LOWER_BUS_PHASE_B = st.slider('LOWER BUS PHASE B Temperature', 0.00, 100.00, 50.00)
            LOWER_BUS_PHASE_C = st.slider('LOWER BUS PHASE C Temperature', 0.00, 100.00, 50.00)
        with col2:
            OUTGOING_PHASE_A = st.slider('OUTGOING PHASE A Temperature', 0.00, 100.00, 50.00)
            OUTGOING_PHASE_B = st.slider('OUTGOING PHASE B Temperature', 0.00, 100.00, 50.00)
            OUTGOING_PHASE_C = st.slider('OUTGOING PHASE C Temperature', 0.00, 100.00, 50.00)
            UPPER_BUS_PD = st.slider('UPPER BUS PD', 0.00, 10000.00, 100.00)
            LOWER_BUS_PD = st.slider('LOWER BUS PD', 0.00, 10000.00, 100.00)
            SPOUT_PD = st.slider('SPOUT PD', 0.00, 10000.00, 100.00)
            OUTGOING_PD = st.slider('OUTGOING PD', 0.00, 10000.00, 100.00)
        data = {
                'Start' : Start_Time,
                'End' : End_Time,
                'UPPER_BUS_PHASE_A': UPPER_BUS_PHASE_A,
                'UPPER_BUS_PHASE_B': UPPER_BUS_PHASE_B,
                'UPPER_BUS_PHASE_C': UPPER_BUS_PHASE_C,
                'LOWER_BUS_PHASE_A': LOWER_BUS_PHASE_A,
                'LOWER_BUS_PHASE_B': LOWER_BUS_PHASE_B,
                'LOWER_BUS_PHASE_C': LOWER_BUS_PHASE_C,
                'OUTGOING_PHASE_A' : OUTGOING_PHASE_A,
                'OUTGOING_PHASE_B' : OUTGOING_PHASE_B,
                'OUTGOING_PHASE_C' : OUTGOING_PHASE_C,
                'UPPER_BUS_PD': UPPER_BUS_PD,
                'LOWER_BUS_PD' : LOWER_BUS_PD,
                'SPOUT_PD' : SPOUT_PD,
                'OUTGOING_PD': OUTGOING_PD
                }
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()
    SWG_raw = pd.read_csv('20211117_Temp&PD_afterClean_for_modeling.csv')
    SWG_Data = SWG_raw.drop(columns=['Status'])
    df = pd.concat([input_df, SWG_Data],axis=0, ignore_index=True)
    # Selects only the first row (the user input data)
    df = df.iloc[:]

    # Displays the user input features
    st.subheader('User Input features')

    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df.iloc[:1])
    
    if df is not None:
        # Reads in saved classification model
        lstmodel = listmodel('model/')
        # st.write(lstmodel)
        tmp = [i.split('.')[0] for i in lstmodel]
        col1, col2, col3 = st.columns([1,5,1])
        with col2 :
            option = st.selectbox('Select Model:',tmp)
            st.write('You selected model: {}'.format(str(option)))
            lstmodel[tmp.index(option)]
        st_result(lstmodel[tmp.index(option)], df, True)
    
    # # Apply model to make predictions
    # prediction = load_clf.predict(df)

    # #----------------------------------------------------------
    # input_df2 = input_df2[:2] 
    # X_submission = input_df2.iloc[:,1:13].to_numpy()

    # prediction2 = load_clf.predict(X_submission)
    # prediction2 = pd.Series(prediction2, name='Severity')
    # df_submission_rfr = pd.concat([input_df2.iloc[:,:1], input_df2.iloc[:,1:13], pd.Series(prediction2)], axis=1)
    # #----------------------------------------------------------

    # st.subheader('Prediction')
    # st.write([prediction])

    # #-----------------------------------------------------------
    # st.write([df_submission_rfr])

    # # Saving our submission file
    # df_submission_rfr.to_excel('20221017_20220805-20220515_NewDecanter_submission_rfr.xlsx', index=False) 

def main():
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