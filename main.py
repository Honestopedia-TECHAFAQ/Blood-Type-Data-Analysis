import streamlit as st
import pandas as pd
import sweetviz as sv

st.title("Blood Type Data Analysis with Sweetviz")

if 'blood_data' not in st.session_state:
    st.session_state.blood_data = None
if 'hospital_data' not in st.session_state:
    st.session_state.hospital_data = None

blood_type_file = st.file_uploader("Upload Blood Type Data (xlsx)", type=["xlsx"])
hospital_stay_file = st.file_uploader("Upload Hospital Stay Data (xlsx)", type=["xlsx"])

def clean_dataframe(df):
    columns_to_clean = ['Date de naissance', 'Unnamed: 16']
    
    for column in columns_to_clean:
        if column in df.columns:
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce') 
            except Exception as e:
                st.warning(f"Could not convert '{column}': {e}")
            if df[column].dtype == 'object':  
                df[column] = df[column].astype(str)  

    return df
if blood_type_file:
    st.session_state.blood_data = pd.read_excel(blood_type_file)
    st.session_state.blood_data.dropna(how='all', inplace=True)  
    st.session_state.blood_data = clean_dataframe(st.session_state.blood_data)  
    st.write("Blood Type Data Loaded:")
    st.write(st.session_state.blood_data)  

if hospital_stay_file:
    st.session_state.hospital_data = pd.read_excel(hospital_stay_file)
    st.session_state.hospital_data.dropna(how='all', inplace=True)  
    st.session_state.hospital_data = clean_dataframe(st.session_state.hospital_data)  
    st.write("Hospital Stay Data Loaded:")
    st.write(st.session_state.hospital_data)  
def has_data(df):
    return df is not None and not df.empty
if st.button("Generate Data Analysis Report"):
    if has_data(st.session_state.blood_data) and has_data(st.session_state.hospital_data):
        report = sv.compare(
            [st.session_state.blood_data, "Blood Type Data"],
            [st.session_state.hospital_data, "Hospital Stay Data"]
        )
        report.show_html("blood_type_analysis_report.html")  
        st.success("Analysis report generated successfully! You can download it below.")
        with open("blood_type_analysis_report.html", "rb") as f:
            st.download_button("Download Analysis Report", f, file_name="blood_type_analysis_report.html")
    else:
        if not has_data(st.session_state.blood_data):
            st.warning("Blood Type Data is empty. Please upload a valid file.")
        if not has_data(st.session_state.hospital_data):
            st.warning("Hospital Stay Data is empty. Please upload a valid file.")
else:
    st.write("Please upload both Excel files to start the analysis.")
