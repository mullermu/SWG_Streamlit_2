from tqdm import tqdm
import pandas as pd
import os
from joblib import load
import joblib
import streamlit as st
import swg
class get_predict_result(object):
    
    def getResult(clfmodel):
        st.write(clfmodel)
        def get_file(path_dataset):
            files = os.listdir(path_dataset)
            files.sort()
            file_list = []
            for file in files:
                path = path_dataset + "/" + file

                if (file.startswith("A")) and (file.endswith(".csv")):
                    file_list.append(path)

            return file_list
        def load_model():
            clf = joblib.load(os.path.join("model/",clfmodel))
            return clf
        def predict_and_save(export = False):
            path_sheet  = "temp/"
            read_columns = ["Start","UPPER_BUS_PHASE_C","OUTGOING_PHASE_B","UPPER_BUS_PD"
            ,"LOWER_BUS_PD","SPOUT_PD","OUTGOING_PD"]

            read_files = get_file(path_sheet)
            clf = load_model()
            all_df = {}
            for i,file in enumerate(tqdm(read_files)):
                filename = file.split("/")[-1].split(".")[0]
                st.write(filename)
                if filename != 'A16':
                    rawdf=pd.read_csv(file, index_col=0)
                    df = pd.read_csv(file, usecols=read_columns) #)
                    rs = swg.Swg(rawdf)
                    X = rs.scale()
                    st.write('Prediction data')
                    # st.table(X)
                    st.table(df)
                    model = joblib.load(os.path.join("model/",clfmodel))
                    # z = model.predict(X)
                    z = model.predict(df.drop(columns='Start'))
                    
                    res = pd.concat([rawdf,pd.DataFrame(z+1,columns=['Status'])],axis=1)
                    st.table(res.head())
                    all_df[file.split("/")[-1].split(".")[0]] = clf.predict(df.iloc[:,1:].values)
                    if export :     
                        res.to_csv(f"output/Predicted Results/{filename}.csv",index=False)
                        # res.to_excel("../output/Predicted Results/Results.xlsx", sheet_name=filename, index=False)


                        # import openpyxl
                        # import csv

                        # wb = openpyxl.Workbook()
                        # # del wb[wb.sheetnames[0]]        # Remove the default 'Sheet1'

                        # with open("../output/Predicted Results/Results.xlsx") as f_input:
                        #         ws = wb.create_sheet(title=os.path.basename(filename))
                                
                        #         for row in csv.reader(res, delimiter=';'):
                        #             ws.append(row)
                
                        # wb.save('../output/Predicted Results/Results.xlsx')
                    
                else :
                    
                    df = pd.read_csv(file)#, usecols=read_columns)


            df = pd.concat([df["Start"],pd.DataFrame.from_dict(all_df)],axis=1)
            df2 = df.copy()
            df2.iloc[:,1:] = df2.iloc[:,1:] +1
            if export :
                df2.to_csv("output/Predicted Results/Predict_Dashboard.csv",index=False)
                
            else :
                return df,df2

        predict_and_save(export = True)
