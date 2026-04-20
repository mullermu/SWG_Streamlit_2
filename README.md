# Switchgear Prediction App (v3)

This application is built using Streamlit to visualize switchgear operational data and perform machine-learning-based health prediction.

The system allows users to upload Excel files containing switchgear measurements. The application automatically processes the data, generates required features, and predicts switchgear health conditions using a trained model.

User authentication is implemented using Microsoft Authentication Library (MSAL) integrated with Azure Active Directory.

---

# Installation

## 1. Install dependencies

pip install -r requirements.txt

## 2. Run the application

streamlit run app.py

---

# Python Runtime

For deployment environments such as Streamlit Community Cloud, specify the Python version.

Create a file named:

runtime.txt

Content:

python-3.11

This ensures compatibility with TensorFlow 2.20.0.

---

# TensorFlow Installation

If TensorFlow fails to install in some environments, install the CPU version manually:

pip install tensorflow-cpu==2.20.0 --only-binary=:all:



# New Features in Version 3

Version 2 introduces automatic processing for uploaded Excel files.

After uploading files, the application runs:

split_and_savefile(uploaded_file1).split()
split_and_savefile(uploaded_file2).split()

The system automatically:

1. Read Excel data
2. Process and clean the data
3. Generate required machine learning features

Generated features include:

Time Features
- Start
- End

Temperature Features
- 9 temperature sensor values

Partial Discharge (PD) Features
- 4 PD measurements

Electrical Features
- Power
- Frequency
- Voltage

These features are required by the prediction model used in Version 2.

To identify new code sections added in this version, search for:

# addition v3

---

# Application Structure

Main application file:

app.py

Main function:

func_main()

This function controls the full application logic for Version 2 and is integrated into Tab 4 of the Streamlit interface.

---

# Project Structure

project_root

app.py  
requirements.txt  
runtime.txt  

source_code/  
    model_bundle_switchgear/   -> trained model files  
    util/                      -> utility functions  

data/  
    fail_case/  
        failure case data (2019 A6, 2025 A15)

    raw_data/  
        A1.csv - A31.csv  
        created after uploading Excel

    output/  
        A1.csv - A31.csv  
        prediction results

---

# Data Workflow

Upload Excel  
↓  
Split and generate required features  
↓  
Save processed data → data/raw_data/  
↓  
Run prediction model  
↓  
Save results → data/output/  
↓  
Visualize results in Streamlit dashboard