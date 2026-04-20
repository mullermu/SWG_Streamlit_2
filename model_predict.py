from tqdm import tqdm
import pandas as pd
import os
from joblib import load
import joblib
import streamlit as st
import swg


# class get_predict_result(object):
#     def getResult(clfmodel, data, sim = False):
#         def get_file(path_dataset):
#             files = os.listdir(path_dataset)
#             files.sort()
#             file_list = []
#             for file in files:
#                 path = path_dataset + "/" + file

#                 if (file.startswith("A")) and (file.endswith(".csv")):
#                     file_list.append(path)

#             return file_list
#         @st.cache_resource
#         def load_model():
#             clf = joblib.load(os.path.join("model/",clfmodel))
#             return clf
#         # def predict_and_save(export = False):
#         #     path_sheet  = "Temp/"
#         #     read_columns = ["A6_Upper_Bus_PhaseA","A6_Upper_Bus_PhaseB","A6_Upper_Bus_PhaseC",
#         #         "A6_Lower_Bus_PhaseA","A6_Lower_Bus_PhaseB","A6_Lower_Bus_PhaseC",
#         #         "A6_Outgoing_PhaseA","A6_Outgoing_PhaseB","A6_Outgoing_PhaseC",
#         #         "PD_Max_Upper", "PD_Max_Lower", "PD_Max_Spout", "PD_Max_Outgoing"]

            
#         #     read_files = get_file(path_sheet)
#         #     for i,file in enumerate(tqdm(read_files)):
#         #         filename = file.split("/")[-1].split(".")[0]
#         #         if filename != 'A16':
#         #             #rawdf=pd.read_csv(file, index_col=0)
#         #             if os.path.getsize(file) == 0:
#         #                 print(f"⚠️ Skip empty file: {file}")
#         #                 continue

#         #             rawdf = pd.read_csv(file, index_col=0)
#         #             rawdf_rename=rawdf.rename(columns={'UPPER_BUS_PHASE_A':'A6_Upper_Bus_PhaseA','UPPER_BUS_PHASE_B':'A6_Upper_Bus_PhaseB', 
#         #                  'UPPER_BUS_PHASE_C':'A6_Upper_Bus_PhaseC','LOWER_BUS_PHASE_A':'A6_Lower_Bus_PhaseA',
#         #                  'LOWER_BUS_PHASE_B':'A6_Lower_Bus_PhaseB','LOWER_BUS_PHASE_C':'A6_Lower_Bus_PhaseC',
#         #                  'OUTGOING_PHASE_A':'A6_Outgoing_PhaseA','OUTGOING_PHASE_B':'A6_Outgoing_PhaseB',
#         #                  'OUTGOING_PHASE_C':'A6_Outgoing_PhaseC','UPPER_BUS_PD':'PD_Max_Upper','LOWER_BUS_PD':'PD_Max_Lower',
#         #                  'SPOUT_PD':'PD_Max_Spout','OUTGOING_PD':'PD_Max_Outgoing'})
#         #             # rs = swg.Swg(rawdf)
#         #             # X = rs.scale()
#         #             model = joblib.load(os.path.join("model/",clfmodel))
#         #             z = model.predict(rawdf_rename[read_columns])
#         #             res = pd.concat([rawdf,pd.DataFrame(z+1,columns=['Status'])],axis=1)
#         #             res.insert(0, "Panel", filename, allow_duplicates=True)
                    
#         #             if export :     
#         #                 res.to_csv(f"output/Predicted Results/{filename}.csv",index=False)
                    
#         #         else :
                    
#         #             df = pd.read_csv(file)#, usecols=read_columns)

#         def predict_and_save(export=False):

#             path_sheet = "Temp/"

#             read_columns = [
#                 "A6_Upper_Bus_PhaseA","A6_Upper_Bus_PhaseB","A6_Upper_Bus_PhaseC",
#                 "A6_Lower_Bus_PhaseA","A6_Lower_Bus_PhaseB","A6_Lower_Bus_PhaseC",
#                 "A6_Outgoing_PhaseA","A6_Outgoing_PhaseB","A6_Outgoing_PhaseC",
#                 "PD_Max_Upper", "PD_Max_Lower", "PD_Max_Spout", "PD_Max_Outgoing"
#             ]

#             read_files = get_file(path_sheet)

#             model = joblib.load(os.path.join("model/", clfmodel))

#             for file in tqdm(read_files):

#                 filename = os.path.basename(file).split(".")[0]

#                 # ------------------------------------------------
#                 # Skip panel A16 (ตาม logic เดิม)
#                 # ------------------------------------------------
#                 if filename == "A16":
#                     print(f"⏭ Skip panel A16")
#                     continue

#                 # ------------------------------------------------
#                 # File validation
#                 # ------------------------------------------------
#                 try:
#                     if not os.path.exists(file):
#                         print(f"File not found: {file}")
#                         continue

#                     if os.path.getsize(file) == 0:
#                         print(f"Empty file skipped: {file}")
#                         continue

#                     rawdf = pd.read_csv(file, index_col=0)

#                     if rawdf.empty:
#                         print(f"No data in file: {file}")
#                         continue

#                 except pd.errors.EmptyDataError:
#                     print(f"Cannot read file (EmptyDataError): {file}")
#                     continue

#                 except Exception as e:
#                     print(f"Error reading {file}: {e}")
#                     continue

#                 # ------------------------------------------------
#                 # Rename columns
#                 # ------------------------------------------------
#                 rawdf_rename = rawdf.rename(columns={
#                     'UPPER_BUS_PHASE_A':'A6_Upper_Bus_PhaseA',
#                     'UPPER_BUS_PHASE_B':'A6_Upper_Bus_PhaseB',
#                     'UPPER_BUS_PHASE_C':'A6_Upper_Bus_PhaseC',
#                     'LOWER_BUS_PHASE_A':'A6_Lower_Bus_PhaseA',
#                     'LOWER_BUS_PHASE_B':'A6_Lower_Bus_PhaseB',
#                     'LOWER_BUS_PHASE_C':'A6_Lower_Bus_PhaseC',
#                     'OUTGOING_PHASE_A':'A6_Outgoing_PhaseA',
#                     'OUTGOING_PHASE_B':'A6_Outgoing_PhaseB',
#                     'OUTGOING_PHASE_C':'A6_Outgoing_PhaseC',
#                     'UPPER_BUS_PD':'PD_Max_Upper',
#                     'LOWER_BUS_PD':'PD_Max_Lower',
#                     'SPOUT_PD':'PD_Max_Spout',
#                     'OUTGOING_PD':'PD_Max_Outgoing'
#                 })

#                 # ------------------------------------------------
#                 # Check required columns
#                 # ------------------------------------------------
#                 missing_cols = [c for c in read_columns if c not in rawdf_rename.columns]

#                 if missing_cols:
#                     print(f"Missing columns in {filename}: {missing_cols}")
#                     continue

#                 # ------------------------------------------------
#                 # Predict
#                 # ------------------------------------------------
#                 z = model.predict(rawdf_rename[read_columns])

#                 res = pd.concat(
#                     [rawdf, pd.DataFrame(z + 1, columns=["Status"])],
#                     axis=1
#                 )

#                 res.insert(0, "Panel", filename)

#                 # ------------------------------------------------
#                 # Export
#                 # ------------------------------------------------
#                 if export:
#                     out_path = f"output/Predicted Results/{filename}.csv"
#                     os.makedirs(os.path.dirname(out_path), exist_ok=True)
#                     res.to_csv(out_path, index=False)

#                     print(f"Saved: {out_path}")


#         def predict_sim():
            
#             rawdf=data
#             rawdf_rename=rawdf.rename(columns={'UPPER_BUS_PHASE_A':'A6_Upper_Bus_PhaseA','UPPER_BUS_PHASE_B':'A6_Upper_Bus_PhaseB', 
#                     'UPPER_BUS_PHASE_C':'A6_Upper_Bus_PhaseC','LOWER_BUS_PHASE_A':'A6_Lower_Bus_PhaseA',
#                     'LOWER_BUS_PHASE_B':'A6_Lower_Bus_PhaseB','LOWER_BUS_PHASE_C':'A6_Lower_Bus_PhaseC',
#                     'OUTGOING_PHASE_A':'A6_Outgoing_PhaseA','OUTGOING_PHASE_B':'A6_Outgoing_PhaseB',
#                     'OUTGOING_PHASE_C':'A6_Outgoing_PhaseC','UPPER_BUS_PD':'PD_Max_Upper','LOWER_BUS_PD':'PD_Max_Lower',
#                     'SPOUT_PD':'PD_Max_Spout','OUTGOING_PD':'PD_Max_Outgoing'})
            
#             read_columns = ["A6_Upper_Bus_PhaseA","A6_Upper_Bus_PhaseB","A6_Upper_Bus_PhaseC",
#                 "A6_Lower_Bus_PhaseA","A6_Lower_Bus_PhaseB","A6_Lower_Bus_PhaseC",
#                 "A6_Outgoing_PhaseA","A6_Outgoing_PhaseB","A6_Outgoing_PhaseC",
#                 "PD_Max_Upper", "PD_Max_Lower", "PD_Max_Spout", "PD_Max_Outgoing"]
#             # rs = swg.Swg(rawdf)
#             # predict_df = rs.scale()
            
#             # predict_df = pd.DataFrame(X).iloc[:1]
            
#             model = joblib.load(os.path.join("model/",clfmodel))
#             z = model.predict(rawdf_rename[read_columns])
#             st.write(z)
#             res = pd.concat([rawdf,pd.DataFrame(z+1,columns=['Status'])],axis=1)
#             res.insert(0, "Panel", "Simulation", allow_duplicates=True)
            
#             st.write(res['Status'])

#         if sim is not True:
#             predict_and_save(export = True)
#         else:
#             predict_sim()

from tqdm import tqdm
import pandas as pd
import os
import joblib
import streamlit as st
import swg


class get_predict_result(object):

    def getResult(clfmodel, data, sim=False):

        # ------------------------------------------------
        # Get CSV files from Temp/
        # ------------------------------------------------
        def get_file(path_dataset):
            files = os.listdir(path_dataset)
            files.sort()

            file_list = []

            for file in files:
                path = path_dataset + "/" + file

                if file.startswith("A") and file.endswith(".csv"):
                    file_list.append(path)

            return file_list

        # ------------------------------------------------
        # CLEAN FUNCTION (สำคัญมาก 🔥)
        # ------------------------------------------------
        def clean_for_model(df, cols):

            df[cols] = (
                df[cols]
                .replace(r'^\s*$', pd.NA, regex=True)   # space -> NaN
                .apply(pd.to_numeric, errors='coerce') # to float
                .fillna(0)                              # fill NaN
            )

            return df

        # ============================================================
        # PREDICT FROM FILES (Temp/)
        # ============================================================
        def predict_and_save(export=False):

            path_sheet = "Temp/"

            read_columns = [
                "A6_Upper_Bus_PhaseA", "A6_Upper_Bus_PhaseB", "A6_Upper_Bus_PhaseC",
                "A6_Lower_Bus_PhaseA", "A6_Lower_Bus_PhaseB", "A6_Lower_Bus_PhaseC",
                "A6_Outgoing_PhaseA", "A6_Outgoing_PhaseB", "A6_Outgoing_PhaseC",
                "PD_Max_Upper", "PD_Max_Lower", "PD_Max_Spout", "PD_Max_Outgoing"
            ]

            read_files = get_file(path_sheet)

            model = joblib.load(os.path.join("model/", clfmodel))

            for file in tqdm(read_files):

                filename = os.path.basename(file).split(".")[0]

                # ------------------------------------------------
                # Skip panel A16
                # ------------------------------------------------
                if filename == "A16":
                    print(f"⏭ Skip panel A16")
                    continue

                # ------------------------------------------------
                # File validation
                # ------------------------------------------------
                try:
                    if not os.path.exists(file):
                        print(f"File not found: {file}")
                        continue

                    if os.path.getsize(file) == 0:
                        print(f"Empty file skipped: {file}")
                        continue

                    rawdf = pd.read_csv(file, index_col=0)

                    if rawdf.empty:
                        print(f"No data in file: {file}")
                        continue

                except pd.errors.EmptyDataError:
                    print(f"Cannot read file (EmptyDataError): {file}")
                    continue

                except Exception as e:
                    print(f"Error reading {file}: {e}")
                    continue

                # ------------------------------------------------
                # Rename columns
                # ------------------------------------------------
                rawdf_rename = rawdf.rename(columns={
                    'UPPER_BUS_PHASE_A': 'A6_Upper_Bus_PhaseA',
                    'UPPER_BUS_PHASE_B': 'A6_Upper_Bus_PhaseB',
                    'UPPER_BUS_PHASE_C': 'A6_Upper_Bus_PhaseC',
                    'LOWER_BUS_PHASE_A': 'A6_Lower_Bus_PhaseA',
                    'LOWER_BUS_PHASE_B': 'A6_Lower_Bus_PhaseB',
                    'LOWER_BUS_PHASE_C': 'A6_Lower_Bus_PhaseC',
                    'OUTGOING_PHASE_A': 'A6_Outgoing_PhaseA',
                    'OUTGOING_PHASE_B': 'A6_Outgoing_PhaseB',
                    'OUTGOING_PHASE_C': 'A6_Outgoing_PhaseC',
                    'UPPER_BUS_PD': 'PD_Max_Upper',
                    'LOWER_BUS_PD': 'PD_Max_Lower',
                    'SPOUT_PD': 'PD_Max_Spout',
                    'OUTGOING_PD': 'PD_Max_Outgoing'
                })

                # ------------------------------------------------
                # Check required columns
                # ------------------------------------------------
                missing_cols = [c for c in read_columns if c not in rawdf_rename.columns]

                if missing_cols:
                    print(f"Missing columns in {filename}: {missing_cols}")
                    continue

                # ------------------------------------------------
                # 🔥 CLEAN DATA BEFORE PREDICT
                # ------------------------------------------------
                rawdf_rename = clean_for_model(rawdf_rename, read_columns)

                # ------------------------------------------------
                # Predict
                # ------------------------------------------------
                z = model.predict(rawdf_rename[read_columns])

                res = pd.concat(
                    [rawdf, pd.DataFrame(z + 1, columns=["Status"])],
                    axis=1
                )

                res.insert(0, "Panel", filename)

                # ------------------------------------------------
                # Export
                # ------------------------------------------------
                if export:
                    out_path = f"output/Predicted Results/{filename}.csv"
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)

                    res.to_csv(out_path, index=False)

                    print(f"Saved: {out_path}")

        # ============================================================
        # SIMULATION MODE (ใช้ DataFrame ที่ส่งมา)
        # ============================================================
        def predict_sim():

            rawdf = data

            rawdf_rename = rawdf.rename(columns={
                'UPPER_BUS_PHASE_A': 'A6_Upper_Bus_PhaseA',
                'UPPER_BUS_PHASE_B': 'A6_Upper_Bus_PhaseB',
                'UPPER_BUS_PHASE_C': 'A6_Upper_Bus_PhaseC',
                'LOWER_BUS_PHASE_A': 'A6_Lower_Bus_PhaseA',
                'LOWER_BUS_PHASE_B': 'A6_Lower_Bus_PhaseB',
                'LOWER_BUS_PHASE_C': 'A6_Lower_Bus_PhaseC',
                'OUTGOING_PHASE_A': 'A6_Outgoing_PhaseA',
                'OUTGOING_PHASE_B': 'A6_Outgoing_PhaseB',
                'OUTGOING_PHASE_C': 'A6_Outgoing_PhaseC',
                'UPPER_BUS_PD': 'PD_Max_Upper',
                'LOWER_BUS_PD': 'PD_Max_Lower',
                'SPOUT_PD': 'PD_Max_Spout',
                'OUTGOING_PD': 'PD_Max_Outgoing'
            })

            read_columns = [
                "A6_Upper_Bus_PhaseA", "A6_Upper_Bus_PhaseB", "A6_Upper_Bus_PhaseC",
                "A6_Lower_Bus_PhaseA", "A6_Lower_Bus_PhaseB", "A6_Lower_Bus_PhaseC",
                "A6_Outgoing_PhaseA", "A6_Outgoing_PhaseB", "A6_Outgoing_PhaseC",
                "PD_Max_Upper", "PD_Max_Lower", "PD_Max_Spout", "PD_Max_Outgoing"
            ]

            model = joblib.load(os.path.join("model/", clfmodel))

            # CLEAN DATA
            rawdf_rename = clean_for_model(rawdf_rename, read_columns)

            z = model.predict(rawdf_rename[read_columns])

            res = pd.concat(
                [rawdf, pd.DataFrame(z + 1, columns=['Status'])],
                axis=1
            )

            res.insert(0, "Panel", "Simulation")

            st.write(res['Status'])

        # ============================================================
        # RUN MODE
        # ============================================================
        if sim is not True:
            predict_and_save(export=True)
        else:
            predict_sim()