# regressly/econometric_data/model_date_selection.py


import os
import json
import pandas as pd
import streamlit as st
from econometric_data.regression_info import regression_info, display_regression_info

# Set up paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "uploaded_files")
JSON_FILE = os.path.join(DATA_DIR, "ingested_files.json")
OUTPUT_FILE = os.path.join(CURRENT_DIR, "date_and_model_selection.json")

def display_model_date_selection():
    """
    Display model and date selection in Streamlit.
    """
    # Load datasets from JSON
    try:
        with open(JSON_FILE, 'r') as f:
            datasets = json.load(f)
    except FileNotFoundError:
        st.error("No datasets found. Please upload files in Step 1.")
        return
    except json.JSONDecodeError:
        st.error("Error reading JSON file. Please ensure it's valid.")
        return

    # Step 2 Header
    st.markdown(
        "<h1 style='color: #1E90FF; text-align: center;'>Step 2: Model and Date Selection</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='color: #4682B4;'>Select your regression model and configure dataset options.</h3>",
        unsafe_allow_html=True,
    )

    # Dropdown for model selection
    st.markdown(
        "<h4 style='color: #5A9BD5;'>Select a Regression Model</h4>",
        unsafe_allow_html=True,
    )
    model = st.selectbox("Choose a Model", options=list(regression_info.keys()))

    # Display model details dynamically
    if model:
        st.markdown(
            "<h4 style='color: #7BAFD4;'>Model Information</h4>",
            unsafe_allow_html=True,
        )
        display_regression_info(model)

    # Frequency selection (only for models that require time frequency)
    if model in ["Linear Regression", "ARIMA"]:
        st.markdown(
            "<h4 style='color: #5A9BD5;'>Select Frequency</h4>",
            unsafe_allow_html=True,
        )
        frequency = st.selectbox(
            "Choose Frequency", options=["Daily", "Weekly", "Monthly", "Quarterly", "Annually"]
        )
    else:
        frequency = None

    # Dataset and Date Column Selection
    st.markdown(
        "<h4 style='color: #4A90E2;'>Select Date Columns for Each Dataset</h4>",
        unsafe_allow_html=True,
    )

    selected_date_columns = {}
    for file_name, details in datasets.items():
        # Display file name with color
        st.markdown(
            f"<p style='color: #7BAFD4; font-weight: bold;'>{file_name}</p>",
            unsafe_allow_html=True,
        )
        # Display styled label for "date" selection
        st.markdown(
            f"Choose <span style='color: #FF5733; font-weight: bold;'>date</span> column for {file_name}:",
            unsafe_allow_html=True,
        )
        # Dropdown for date column selection
        column = st.selectbox(
            f"Date column for {file_name}",  # Simple text for compatibility
            options=details["headers"],
            key=f"date_column_{file_name}",
        )
        selected_date_columns[file_name] = {"path": details["path"], "date_column": column}

    # Submit button
    if st.button("Submit Selections"):
        # Prepare data for saving
        selection_data = {
            "model": model,
            "frequency": frequency,
            "datasets": [
                {
                    "file_name": file_name,
                    "path": details["path"],
                    "date_column": selected_date_columns[file_name]["date_column"],
                }
                for file_name, details in datasets.items()
            ],
        }

        try:
            # Write to output JSON file
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(selection_data, f, indent=4)

            st.success("Selections saved successfully!")
            st.json(selection_data)  # Display saved data
        except Exception as e:
            st.error(f"Error saving selections: {e}")
