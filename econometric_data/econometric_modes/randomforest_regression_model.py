# regressly/econometric_data/econometric_modes/randomforest_regression_model.py


import os
import json
import pandas as pd
import streamlit as st

def load_selection_data(json_file="econometric_data/date_and_model_selection.json"):
    """
    Load the JSON file containing datasets and selected model type.
    """
    if not os.path.exists(json_file):
        st.error("JSON file not found. Please complete Step 2 first.")
        return None
    with open(json_file, 'r') as f:
        return json.load(f)

def display_widgets():
    """
    Display widgets for Random Forest Regression variable selection.
    """
    selection_data = load_selection_data()
    if not selection_data:
        return

    datasets = selection_data["datasets"]

    all_columns = {}
    date_columns = set()

    for dataset in datasets:
        file_path = dataset["path"]
        date_column = dataset["date_column"]
        date_columns.add(date_column)

        df = pd.read_csv(file_path)
        for column in df.columns:
            all_columns[column] = {
                "file_name": dataset["file_name"],
                "file_path": dataset["path"]
            }

    column_names = sorted([col for col in all_columns.keys() if col not in date_columns])

    # Streamlit widgets
    st.header("Random Forest Regression Variable Selection")

    y_variable = st.selectbox("Select the Dependent Variable (Y):", options=column_names)

    x_categorical = st.multiselect(
        "Select Categorical Independent Variables (X):",
        options=column_names,
    )

    x_continuous = st.multiselect(
        "Select Continuous Independent Variables (X):",
        options=column_names,
    )

    n_estimators = st.slider(
        "Number of Trees (n_estimators):",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
    )

    if st.button("Submit Selections"):
        if not y_variable or not (x_categorical or x_continuous):
            st.error("Please select the dependent variable and at least one independent variable.")
            return

        # Create the JSON structure
        variable_data = {
            "model": "Random Forest Regression",
            "parameters": {
                "n_estimators": n_estimators,
            },
            "y": {
                "variable": y_variable,
                "file_name": all_columns[y_variable]["file_name"],
                "file_path": all_columns[y_variable]["file_path"],
            },
            "x": [],
        }

        # Add categorical variables to the JSON
        for x_var in x_categorical:
            variable_data["x"].append({
                "variable": x_var,
                "type": "categorical",
                "file_name": all_columns[x_var]["file_name"],
                "file_path": all_columns[x_var]["file_path"],
            })

        # Add continuous variables to the JSON
        for x_var in x_continuous:
            variable_data["x"].append({
                "variable": x_var,
                "type": "continuous",
                "file_name": all_columns[x_var]["file_name"],
                "file_path": all_columns[x_var]["file_path"],
            })

        # Save to JSON file
        output_file = "econometric_data/selected_variables.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(variable_data, f, indent=4)

        st.success(f"Selections saved to {output_file}")
        st.json(variable_data)
