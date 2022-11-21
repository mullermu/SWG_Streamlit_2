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
        scl = StandardScaler()
        X = scl.fit_transform(df.iloc[:,2:8].values)
        # X = df.iloc[:,2:8].values
        st.write('StandardScalered')
        st.table(X)
        if df.shape[1] == 9:
            
            y = df.iloc[:,8].values
            
            st.write('StandardScalered')
            st.table(y)
            return X,y
        else: return X 
        
    def acc(self,pred,true): return accuracy_score(true,pred)
    


