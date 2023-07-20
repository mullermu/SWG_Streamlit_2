from tqdm import tqdm
import pandas as pd
import os
from joblib import load
import joblib
import streamlit as st
import swg
class get_predict_result(object):
    
    def getResult(clfmodel, data, sim = False):
        # st.write(clfmodel)
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
            path_sheet  = "Temp/"
            read_columns = ["Start","UPPER_BUS_PHASE_C","OUTGOING_PHASE_B","UPPER_BUS_PD"
            ,"LOWER_BUS_PD","SPOUT_PD","OUTGOING_PD"]

            read_files = get_file(path_sheet)
            # clf = load_model()
            # all_df = {}
            for i,file in enumerate(tqdm(read_files)):
                filename = file.split("/")[-1].split(".")[0]
                # st.write(filename)
                if filename != 'A16':
                    rawdf=pd.read_csv(file, index_col=0)

                    # #Find Lastrow
                    # lastrow = len(rawdf.index)
                    
                    # #Import dataset file
                    # SWG_raw = pd.read_csv('Dataset/20230712_2016-2023_Dataset.csv')
                    # SWG_Data = SWG_raw.drop(columns=['Status'])

                    
                    # #concat data and dataset for Scaler
                    # df = pd.concat([rawdf, SWG_Data],axis=0, ignore_index=True)
                    

                    # df = pd.read_csv(file, usecols=read_columns) #)

                    rs = swg.Swg(rawdf)
                    X = rs.scale()

                    #Predict only data by dropping dataset using last row
                    # predict_df = pd.DataFrame(X).iloc[:lastrow]
                    # st.table(X.head())


                    model = joblib.load(os.path.join("model/",clfmodel))
                    z = model.predict(X)

                    
                    res = pd.concat([rawdf,pd.DataFrame(z+1,columns=['Status'])],axis=1)
                    res.insert(0, "Panel", filename, allow_duplicates=True)
                    
                    # st.table(res.head())
                    # all_df[file.split("/")[-1].split(".")[0]] = clf.predict(df.iloc[:,1:].values)
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


            # df = pd.concat([df["Start"],pd.DataFrame.from_dict(all_df)],axis=1)
            # df2 = df.copy()
            # df2.iloc[:,1:] = df2.iloc[:,1:] +1
            # if export :
            #     df2.to_csv("output/Predicted Results/Predict_Dashboard.csv",index=False)
                
            # else :
            #     return df,df2
        def predict_sim():
            rawdf=data
            # rawdf=pd.read_csv(data, usecols=read_columns)
            rs = swg.Swg(rawdf)
            X = rs.scale()
            # st.write('Used Standard Scaler to predict data')
            # st.table(X)
            # st.table(df)
            predict_df = pd.DataFrame(X).iloc[:1]
            model = joblib.load(os.path.join("model/",clfmodel))
            z = model.predict(predict_df)
            # z = model.predict(df.drop(columns='Start'))
            res = pd.concat([predict_df,pd.DataFrame(z+1,columns=['Status'])],axis=1)
            res.insert(0, "Panel", "Simulation", allow_duplicates=True)
            
            st.write(res['Status'])
        if sim is not True:
            predict_and_save(export = True)
        else:
            predict_sim()

