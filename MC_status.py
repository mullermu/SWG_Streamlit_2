from string import whitespace
import streamlit as st 
from time import sleep
from tqdm import tqdm
import pandas as pd
import os

class MC_status(object):
    def st_status():

        def status_color(status):
            def inner_status_color():
                if status==1: return st.success("State A")
                elif status==2: return st.info("State B")
                elif status==3: return st.warning("State C")
                else:  return st.error("State D")
            return inner_status_color()

        def read_machine_status(MCName):
            path_sheet  = f"output/Predicted Results/{MCName}.csv"
            # read_files = get_file(path_sheet)
            # for i,file in enumerate(tqdm(read_files)):
                # filename = file.split("/")[-1].split(".")[0]
                # st.write(filename)
            if MCName != 'A16':
                df=pd.read_csv(path_sheet, index_col=0)
                mcStatus = df['Status'].iat[-1]
            else:
                # df=pd.read_csv(path_sheet, index_col=0)
                mcStatus = 1
            return mcStatus 
                
        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            st.markdown('**A1**')
            status_color(read_machine_status("A1"))
        with b2:
            st.markdown('**A2**')
            status_color(read_machine_status("A2"))
        with b3:
            st.markdown('**A3**')
            status_color(read_machine_status("A3"))
        with b4:
            st.markdown('**A4**')
            status_color(read_machine_status("A4"))
        with b5:
            st.markdown('**A5**')
            status_color(read_machine_status("A5"))
        b6, b7, b8, b9, b10 = st.columns(5)
        with b6:
            st.markdown('**A6**')
            status_color(read_machine_status("A6"))
        with b7:
            st.markdown('**A7**')
            status_color(read_machine_status("A7"))
        with b8:
            st.markdown('**A8**')
            status_color(read_machine_status("A8"))
        with b9:
            st.markdown('**A9**')
            status_color(read_machine_status("A9"))
        with b10:
            st.markdown('**A10**')
            status_color(read_machine_status("A10"))
        b11, b12, b13, b14, b15 = st.columns(5)
        with b11:
            st.markdown('**A11**')
            status_color(read_machine_status("A11"))
        with b12:
            st.markdown('**A12**')
            status_color(read_machine_status("A12"))
        with b13:
            st.markdown('**A13**')
            status_color(read_machine_status("A13"))
        with b14:
            st.markdown('**A14**')
            status_color(read_machine_status("A14"))
        with b15:
            st.markdown('**A15**')
            status_color(read_machine_status("A15"))
        b16, b17, b18, b19, b20 = st.columns(5)
        with b16:
            st.markdown('**A16**')
            status_color(read_machine_status("A16"))
        with b17:
            st.markdown('**A18**')
            status_color(read_machine_status("A18"))
        with b18:
            st.markdown('**A19**')
            status_color(read_machine_status("A19"))
        with b19:
            st.markdown('**A20**')
            status_color(read_machine_status("A20"))
        with b20:
            st.markdown('**A21**')
            status_color(read_machine_status("A21"))
        b21, b22, b23, b24, b25 = st.columns(5)
        with b21:
            st.markdown('**A22**')
            status_color(read_machine_status("A22"))
        with b22:
            st.markdown('**A23**')
            status_color(read_machine_status("A23"))
        with b23:
            st.markdown('**A24**')
            status_color(read_machine_status("A24"))
        with b24:
            st.markdown('**A25**')
            status_color(read_machine_status("A25"))
        with b25:
            st.markdown('**A26**')
            status_color(read_machine_status("A26"))
        b26, b27, b28, b29, b30 = st.columns(5)
        with b26:
            st.markdown('**A27**')
            status_color(read_machine_status("A27"))
        with b27:
            st.markdown('**A28**')
            status_color(read_machine_status("A28"))
        with b28:
            st.markdown('**A29**')
            status_color(read_machine_status("A29"))
        with b29:
            st.markdown('**A30**')
            status_color(read_machine_status("A30"))
        with b30:
            st.markdown('**A31**')
            status_color(read_machine_status("A31"))

        
        return     b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20, b21, b22, b23, b24, b25, b26, b27, b28,b29, b30

    def sum_status():
        stageA=0
        stageB=0
        stageC=0
        stageD=0
        
        def get_file(path_dataset):
            files = os.listdir(path_dataset)
            files.sort()
            file_list = []
            for file in files:
                path = path_dataset + "/" + file

                if (file.startswith("A")) and (file.endswith(".csv")):
                    file_list.append(path)

            return file_list

        path_sheet  = "output/Predicted Results/"
        read_files = get_file(path_sheet)
        for i,file in enumerate(tqdm(read_files)):
            filename = file.split("/")[-1].split(".")[0]
            if filename != 'A16':
                df=pd.read_csv(file, index_col=0)
                mcStatus = df['Status'].iat[-1]
            else:
                # df=pd.read_csv(path_sheet, index_col=0)
                mcStatus = 1

            if mcStatus == 1:
                stageA=stageA+1
            elif mcStatus == 2:
                stageB=stageB+1
            elif mcStatus == 3:
                stageC=stageC+1
            else: 
                stageD=stageD+1
        return stageA, stageB, stageC, stageD