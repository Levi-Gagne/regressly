import os
import json
import pandas as pd
import streamlit as st
from pathlib import Path

# Constants
JSON_FILE = "econometric_module/ingested_files.json"

def streamlit_file_uploader():
    """Function to handle file uploading in Streamlit."""
    # Set current directory
    current_path = Path.cwd()
    st.write(f"Current Directory: `{current_path}`")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])
    if uploaded_file:
        # Read the file and extract headers
        df = pd.read_csv(uploaded_file, nrows=0)
        headers = df.columns.tolist()
        file_name = uploaded_file.name

        # Ensure JSON file exists
        if not Path(JSON_FILE).exists():
            with open(JSON_FILE, 'w') as f:
                json.dump({}, f)

        # Append uploaded file info to JSON
        try:
            with open(JSON_FILE, 'r') as f:
                files = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            files = {}

        files[file_name] = {
            "path": str(current_path / file_name),
            "headers": headers
        }

        with open(JSON_FILE, 'w') as f:
            json.dump(files, f, indent=4)

        # Save uploaded file to the current directory
        with open(current_path / file_name, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Display success message
        st.success(f"File `{file_name}` uploaded successfully!")
        st.json(files)

    # View uploaded files
    if st.button("View Uploaded Files"):
        if Path(JSON_FILE).exists():
            with open(JSON_FILE, 'r') as f:
                files = json.load(f)
            st.json(files)
        else:
            st.warning("No files uploaded yet!")
