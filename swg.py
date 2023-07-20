from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import streamlit as st
import numpy as np
import pandas as pd

class Swg(object):

    def __init__(self,data):
        
        self.data = data

    def scale(self):
        df = self.data
        #Find Lastrow
        lastrow = len(df.index)
        SWG_Data = pd.read_csv("Dataset/SWG_Dataset.csv")
        SWG_Data = SWG_Data.drop(columns=['Start time','End time','Severity'])
         
        # SWG_Data.set_axis([read_columns], axis='columns', inplace=True) 

        #concat data and dataset for Scaler
        df = pd.concat([df, SWG_Data],axis=0, ignore_index=True)
        st.table(df.head())
        scl = StandardScaler()
        
        read_columns = ["UPPER_BUS_PHASE_A","UPPER_BUS_PHASE_B","UPPER_BUS_PHASE_C",
                "LOWER_BUS_PHASE_A","LOWER_BUS_PHASE_B","LOWER_BUS_PHASE_C",
                "OUTGOING_PHASE_A","OUTGOING_PHASE_B","OUTGOING_PHASE_C",
                "UPPER_BUS_PD", "LOWER_BUS_PD", "SPOUT_PD", "OUTGOING_PD"]

        X = scl.fit_transform(df[read_columns].values)
        

        if df.shape[1] == 9:
            
            y = df.iloc[:,8].values
            return X,y
        else: 
            X = pd.DataFrame(X).iloc[:lastrow]
            return X 
        
    def acc(self,pred,true): return accuracy_score(true,pred)
    
