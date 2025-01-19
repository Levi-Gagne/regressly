# regressly/econometric_data/econometric_modes/logistic_regression_model.py

import os
import json
import pandas as pd
import streamlit as st

# Load JSON selection data
def load_selection_data(json_file="econometric_data/date_and_model_selection.json"):
    if not os.path.exists(json_file):
        st.error(f"File not found: {json_file}")
        return None
    with open(json_file, 'r') as f:
        return json.load(f)

# Display widgets for logistic regression variable selection
def display_widgets():
    selection_data = load_selection_data()
    if not selection_data:
        return

    datasets = selection_data["datasets"]

    # Extract available columns for each dataset
    all_columns = {}
    for dataset in datasets:
        file_path = dataset["path"]
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Error loading file: {file_path}. {e}")
            continue

        for column in df.columns:
            all_columns[column] = {
                "file_name": dataset["file_name"],
                "file_path": file_path
            }

    column_names = sorted(all_columns.keys())

    # Display headers
    st.header("Select Variables for Logistic Regression")
    st.write("Choose the dependent variable (Y), and independent variables (X), categorized as categorical or continuous.")

    # Dependent variable
    y_variable = st.selectbox("Select Dependent Variable (Y)", options=column_names)

    # Independent variables
    x_categorical = st.multiselect("Select Categorical Independent Variables (X)", options=column_names)
    x_continuous = st.multiselect("Select Continuous Independent Variables (X)", options=column_names)

    # Validation: Ensure Y is not in X variables
    if y_variable in x_categorical or y_variable in x_continuous:
        st.error("Dependent variable (Y) cannot also be an independent variable (X). Please revise your selections.")
        return

    # Validation: Ensure no overlap between categorical and continuous X variables
    overlapping_x = set(x_categorical).intersection(set(x_continuous))
    if overlapping_x:
        st.error(f"Variables {', '.join(overlapping_x)} cannot be both categorical and continuous. Please revise your selections.")
        return

    if st.button("Submit Selections"):
        if not y_variable or not (x_categorical or x_continuous):
            st.error("Please select a dependent variable and at least one independent variable.")
            return

        # Prepare data for saving
        variable_data = {
            "model": "Logistic Regression",
            "y": {
                "variable": y_variable,
                "file_name": all_columns[y_variable]["file_name"],
                "file_path": all_columns[y_variable]["file_path"]
            },
            "x": []
        }

        # Add categorical variables to the JSON
        for x_var in x_categorical:
            variable_data["x"].append({
                "variable": x_var,
                "type": "categorical",
                "file_name": all_columns[x_var]["file_name"],
                "file_path": all_columns[x_var]["file_path"]
            })

        # Add continuous variables to the JSON
        for x_var in x_continuous:
            variable_data["x"].append({
                "variable": x_var,
                "type": "continuous",
                "file_name": all_columns[x_var]["file_name"],
                "file_path": all_columns[x_var]["file_path"]
            })

        # Save to JSON file
        output_file = "econometric_data/selected_variables.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(variable_data, f, indent=4)

        st.success("Selections saved successfully!")
        st.json(variable_data)  # Display the saved selections for confirmation
