import streamlit as st
import pandas as pd 
import os
from io import BytesIO

# App Setup
st.set_page_config(page_title="File Manager", layout="wide")
st.title("File Converter")
st.write("Change your file between CSV and Excel formats with built-in data cleaning and visualization!")

upload_files = st.file_uploader("Browse your files (CSV or Excel files):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        
        st.write(f"File name : {file.name}")
        st.write(f"File Size : {file.size / 1024:.2f} KB") 

        # Show DataFrame preview
        st.write("Preview of DataFrame")
        st.dataframe(df.head())

        # Data cleaning options FOR THIS FILE
        st.subheader(f"Data Cleaning For Duplicates. {file.name}")
        if st.checkbox(f"Sweep Duplicate Data in {file.name}", key=f"clean_{file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates Removed!")
                    # st.write("Missing Values Filled!")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing Values Filled!")
                    # st.write("Missing Values Filled!")

        # Add a separator between files
        st.markdown("---")
        st.subheader("select Columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


        # file conversion  CSV TO Excel
        st.subheader("Choose Once To Convert Your File")
        file_type = st.radio(f"Convert {file.name} to:",["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if file_type == "CSV":
                df.to_csv(buffer, index=False) 
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"  

            elif file_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {file_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed")           
