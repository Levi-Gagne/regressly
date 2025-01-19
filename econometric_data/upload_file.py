# regressly/econometric_data/upload_file.py

import os
import json
import pandas as pd
import streamlit as st

# Set up paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(CURRENT_DIR, "uploaded_files")
JSON_FILE = os.path.join(UPLOAD_DIR, "ingested_files.json")

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def clear_json_file():
    """Clear the JSON file."""
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump({}, f)
        st.success("JSON file cleared successfully.")
    except Exception as e:
        st.error(f"Error clearing JSON file: {e}")

def load_json_file():
    """Load the JSON file, creating it if it doesn't exist."""
    if not os.path.exists(JSON_FILE):
        clear_json_file()
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.warning("JSON file is invalid or empty. Resetting.")
        clear_json_file()
        return {}

def write_to_json(files_metadata):
    """Write file metadata to the JSON file."""
    try:
        # Write metadata to JSON
        with open(JSON_FILE, 'w') as f:
            json.dump(files_metadata, f, indent=4)
        st.success("JSON file updated successfully.")
    except Exception as e:
        st.error(f"Error writing to JSON file: {e}")

def streamlit_file_uploader():
    """Display file uploader and handle file processing."""
    # Clear JSON File Button
    st.sidebar.write("### Manage JSON File")
    if st.sidebar.button("Clear JSON File"):
        clear_json_file()

    # File Uploader Widget
    st.sidebar.write("### Browse Files")
    uploaded_files = st.sidebar.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

    # Main App: Upload Files Button
    st.write("### Step 1: Upload Your CSV Files")
    if st.button("Upload Files"):
        if uploaded_files:
            files_metadata = {}
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                save_path = os.path.join(UPLOAD_DIR, file_name)

                # Save the file to the upload directory
                with open(save_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                # Extract headers
                try:
                    df = pd.read_csv(save_path, nrows=0)  # Read only headers
                    headers = df.columns.tolist()
                    files_metadata[file_name] = {
                        "path": save_path,
                        "headers": headers
                    }
                except Exception as e:
                    st.error(f"Error reading file {file_name}: {e}")
                    continue

            # Write metadata to JSON
            write_to_json(files_metadata)
        else:
            st.warning("No files selected. Please browse and select files.")

    # Display Current JSON Content
    st.write("### Current JSON File Content")
    files = load_json_file()
    st.json(files)
