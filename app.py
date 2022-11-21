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


def get_csv(df):
    
    csv = df.to_csv(index=False)
    
    return csv
def get_data1(dtfile):
    dtfile.to_csv (r'/Temp/temp.csv', index = False, header=True)

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
    st.write(lstmodel)
    tmp = [i.split('.')[0] for i in lstmodel]
    col1, col2, col3 = st.columns([1,10,1])
    with col2 :
        with st.form(key='my_form'):
            option = st.selectbox('Select Model:',tmp,key="my_option")
            submitted = st.form_submit_button('selected model and predict')
            if submitted:
                st.write('You selected model: {}'.format(str(option)))
    #             return r
                

def st_result(clf):
    df = None
    if clf is not None:
        model_predict.get_predict_result.getResult(clf)
        # model = joblib.load(os.path.join("../model/",clf))
        # z = model.predict(X)
        # res = pd.concat([data,pd.DataFrame(z,columns=['Status'])],axis=1)
        # col1, col2, col3 = st.columns([1,1,1])
        # with col2 :
        #     st.download_button("Download Classification File",get_csv(res),"../output/result_app.csv")
def download_results():
        
    files = [os.path.split(filename) for filename in glob.glob("/output/Predicted Results/*.csv")]

    wb = openpyxl.Workbook()
    del wb[wb.sheetnames[0]]        # Remove the default 'Sheet1'

    for f_path, f_name in files:
        (f_short_name, f_extension) = os.path.splitext(f_name)
        with open(os.path.join(f_path, f_name)) as f_input:
            ws = wb.create_sheet(title=os.path.basename(f_short_name))
            
            for row in csv.reader(f_input):
                ws.append(row)
            
    wb.save('/output/Predicted Results/Results.xlsx')

    with open('/output/Predicted Results/Results.xlsx', 'rb') as my_file:
        st.download_button(label = 'Download Results', data = my_file, file_name = 'Results.xlsx', mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  


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

def main():
    with st.sidebar:  
            data = None
            data = st_header(data)
            clf = st_body()
            if clf is not None and data is True:
                st_result(clf)
                download_results()
            else:
                st.write('Please upload files and select predection model!')
                
            
            

    tab1, tab2 = st.tabs(["Summary", "Details"])
    with tab1:
        st.header("Summary")
        status_body() 
        summary_chart()
    with tab2:
        history_chart()
    

main()
