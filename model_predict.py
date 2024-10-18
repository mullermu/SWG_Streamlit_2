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
        @st.cache_resource
        def load_model():
            clf = joblib.load(os.path.join("model/",clfmodel))
            return clf
        def predict_and_save(export = False):
            path_sheet  = "Temp/"
            
            read_columns = ["Start","UPPER_BUS_PHASE_C","OUTGOING_PHASE_B","UPPER_BUS_PD"
            ,"LOWER_BUS_PD","SPOUT_PD","OUTGOING_PD"]
            
            # read_columns = ["A6_Upper_Bus_PhaseA","A6_Upper_Bus_PhaseB","A6_Upper_Bus_PhaseC",
                "A6_Lower_Bus_PhaseA","A6_Lower_Bus_PhaseB","A6_Lower_Bus_PhaseC",
                "A6_Outgoing_PhaseA","A6_Outgoing_PhaseB","A6_Outgoing_PhaseC",
                "PD_Max_Upper", "PD_Max_Lower", "PD_Max_Spout", "PD_Max_Outgoing"]

            
            read_files = get_file(path_sheet)
            for i,file in enumerate(tqdm(read_files)):
                filename = file.split("/")[-1].split(".")[0]
                if filename != 'A16':
                    rawdf=pd.read_csv(file, index_col=0)
                    # rawdf=rawdf.rename(columns={'UPPER_BUS_PHASE_A':'A6_Upper_Bus_PhaseA','UPPER_BUS_PHASE_B':'A6_Upper_Bus_PhaseB', 
                         'UPPER_BUS_PHASE_C':'A6_Upper_Bus_PhaseC','LOWER_BUS_PHASE_A':'A6_Lower_Bus_PhaseA',
                         'LOWER_BUS_PHASE_B':'A6_Lower_Bus_PhaseB','LOWER_BUS_PHASE_C':'A6_Lower_Bus_PhaseC',
                         'OUTGOING_PHASE_A':'A6_Outgoing_PhaseA','OUTGOING_PHASE_B':'A6_Outgoing_PhaseB',
                         'OUTGOING_PHASE_C':'A6_Outgoing_PhaseC','UPPER_BUS_PD':'PD_Max_Upper','LOWER_BUS_PD':'PD_Max_Lower',
                         'SPOUT_PD':'PD_Max_Spout','OUTGOING_PD':'PD_Max_Outgoing'})
                    rs = swg.Swg(rawdf)
                    X = rs.scale()
                    model = joblib.load(os.path.join("model/",clfmodel))
                    # z = model.predict(rawdf[read_columns])
                    z = model.predict(X)
                    res = pd.concat([rawdf,pd.DataFrame(z+1,columns=['Status'])],axis=1)
                    res.insert(0, "Panel", filename, allow_duplicates=True)
                    
                    if export :     
                        res.to_csv(f"output/Predicted Results/{filename}.csv",index=False)
                    
                else :
                    
                    df = pd.read_csv(file)#, usecols=read_columns)

        def predict_sim():
            
            rawdf=data
            rawdf=rawdf.rename(columns={'UPPER_BUS_PHASE_A':'A6_Upper_Bus_PhaseA','UPPER_BUS_PHASE_B':'A6_Upper_Bus_PhaseB', 
                    'UPPER_BUS_PHASE_C':'A6_Upper_Bus_PhaseC','LOWER_BUS_PHASE_A':'A6_Lower_Bus_PhaseA',
                    'LOWER_BUS_PHASE_B':'A6_Lower_Bus_PhaseB','LOWER_BUS_PHASE_C':'A6_Lower_Bus_PhaseC',
                    'OUTGOING_PHASE_A':'A6_Outgoing_PhaseA','OUTGOING_PHASE_B':'A6_Outgoing_PhaseB',
                    'OUTGOING_PHASE_C':'A6_Outgoing_PhaseC','UPPER_BUS_PD':'PD_Max_Upper','LOWER_BUS_PD':'PD_Max_Lower',
                    'SPOUT_PD':'PD_Max_Spout','OUTGOING_PD':'PD_Max_Outgoing'})
            
            read_columns = ["A6_Upper_Bus_PhaseA","A6_Upper_Bus_PhaseB","A6_Upper_Bus_PhaseC",
                "A6_Lower_Bus_PhaseA","A6_Lower_Bus_PhaseB","A6_Lower_Bus_PhaseC",
                "A6_Outgoing_PhaseA","A6_Outgoing_PhaseB","A6_Outgoing_PhaseC",
                "PD_Max_Upper", "PD_Max_Lower", "PD_Max_Spout", "PD_Max_Outgoing"]
            # rs = swg.Swg(rawdf)
            # predict_df = rs.scale()
            
            # predict_df = pd.DataFrame(X).iloc[:1]
            
            model = joblib.load(os.path.join("model/",clfmodel))
            z = model.predict(rawdf[read_columns])
            res = pd.concat([rawdf,pd.DataFrame(z+1,columns=['Status'])],axis=1)
            res.insert(0, "Panel", "Simulation", allow_duplicates=True)
            
            st.write(res['Status'])

        if sim is not True:
            predict_and_save(export = True)
        else:
            predict_sim()

