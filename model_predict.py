from tqdm import tqdm
import pandas as pd
import os
from joblib import load
import joblib
import streamlit as st
import swg
class get_predict_result(object):
    
    def getResult(clfmodel, data, sim = False):
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
            for i,file in enumerate(tqdm(read_files)):
                filename = file.split("/")[-1].split(".")[0]
                if filename != 'A16':
                    rawdf=pd.read_csv(file, index_col=0)

                    rs = swg.Swg(rawdf)
                    X = rs.scale()

                    model = joblib.load(os.path.join("model/",clfmodel))
                    z = model.predict(X)

                    
                    res = pd.concat([rawdf,pd.DataFrame(z+1,columns=['Status'])],axis=1)
                    res.insert(0, "Panel", filename, allow_duplicates=True)
                    
                    if export :     
                        res.to_csv(f"output/Predicted Results/{filename}.csv",index=False)
                    
                else :
                    
                    df = pd.read_csv(file)#, usecols=read_columns)

        def predict_sim():
            rawdf=data
            rs = swg.Swg(rawdf)
            X = rs.scale()
            predict_df = pd.DataFrame(X).iloc[:1]
            model = joblib.load(os.path.join("model/",clfmodel))
            z = model.predict(predict_df)
            res = pd.concat([predict_df,pd.DataFrame(z+1,columns=['Status'])],axis=1)
            res.insert(0, "Panel", "Simulation", allow_duplicates=True)

            st.write(res['Status'])
        if sim is not True:
            predict_and_save(export = True)
        else:
            predict_sim()

