# regressly/econometric_data/econometric_modes/linear_regression_model.py


import os
import json
import pandas as pd
import statsmodels.api as sm
import streamlit as st
from datetime import datetime

# Load JSON selection data
def load_selection_data(json_file="econometric_data/date_and_model_selection.json"):
    if not os.path.exists(json_file):
        st.error(f"File not found: {json_file}")
        return None
    with open(json_file, 'r') as f:
        return json.load(f)

# Calculate date ranges for datasets
def calculate_date_ranges(datasets):
    date_ranges = {}
    for dataset in datasets:
        file_path = dataset["path"]
        date_column = dataset["date_column"]

        if not os.path.exists(file_path):
            st.error(f"File not found: {file_path}")
            continue

        df = pd.read_csv(file_path)
        if date_column not in df.columns:
            st.error(f"Date column '{date_column}' not found in file: {file_path}")
            continue

        df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
        df = df.dropna(subset=[date_column])

        if df.empty:
            st.error(f"No valid dates found in column '{date_column}' for file: {file_path}")
            continue

        min_date = df[date_column].min()
        max_date = df[date_column].max()
        columns = [col for col in df.columns if col != date_column]

        date_ranges[dataset["file_name"]] = {
            "file_path": file_path,
            "date_column": date_column,
            "min_date": min_date,
            "max_date": max_date,
            "columns": columns
        }
    return date_ranges

# Run regression model
def run_regression_model():
    with open("econometric_data/selected_variables.json", 'r') as f:
        selected_data = json.load(f)

    y_info = selected_data["y"]
    x_info = selected_data["x"]
    start_date = pd.to_datetime(selected_data["start_date"])
    end_date = pd.to_datetime(selected_data["end_date"])

    y_df = pd.read_csv(y_info["file_path"], parse_dates=[y_info["date_column"]])
    y_df.set_index(y_info["date_column"], inplace=True)
    y_df = y_df.loc[start_date:end_date]
    y_column = y_info["variable"]
    y_data = y_df[[y_column]]

    x_data = pd.DataFrame()
    for x_var in x_info:
        x_df = pd.read_csv(x_var["file_path"], parse_dates=[x_var["date_column"]])
        x_df.set_index(x_var["date_column"], inplace=True)
        x_df = x_df.loc[start_date:end_date]
        x_column = x_var["variable"]
        x_data[x_column] = x_df[x_column]

    if not y_data.index.equals(x_data.index):
        st.error("The indices for the dependent and independent variables are not aligned.")
        return

    x_data = sm.add_constant(x_data)
    model = sm.OLS(y_data, x_data).fit()
    st.text(model.summary())

# Display widgets for variable selection
def display_widgets():
    selection_data = load_selection_data()
    if not selection_data:
        return

    datasets = selection_data["datasets"]
    model_type = selection_data["model"]
    frequency = selection_data["frequency"]

    date_ranges = calculate_date_ranges(datasets)

    min_dates = [info["min_date"] for info in date_ranges.values()]
    max_dates = [info["max_date"] for info in date_ranges.values()]

    overall_min_date = max(min_dates)
    overall_max_date = min(max_dates)

    st.header(f"Select Variables for {model_type}")
    st.write(f"Data range: {overall_min_date.date()} to {overall_max_date.date()}")

    # Date selection based on frequency
    if frequency.lower() == "daily":
        start_date = st.date_input(
            "Start Date",
            value=overall_min_date.date(),
            min_value=overall_min_date.date(),
            max_value=overall_max_date.date()
        )
        end_date = st.date_input(
            "End Date",
            value=overall_max_date.date(),
            min_value=overall_min_date.date(),
            max_value=overall_max_date.date()
        )
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
    elif frequency.lower() == "monthly":
        start_month = st.selectbox(
            "Start Month",
            options=[datetime(2000, m, 1).strftime('%B') for m in range(1, 13)],
            index=overall_min_date.month - 1
        )
        start_year = st.selectbox(
            "Start Year",
            options=list(range(overall_min_date.year, overall_max_date.year + 1))
        )
        end_month = st.selectbox(
            "End Month",
            options=[datetime(2000, m, 1).strftime('%B') for m in range(1, 13)],
            index=overall_max_date.month - 1
        )
        end_year = st.selectbox(
            "End Year",
            options=list(range(overall_min_date.year, overall_max_date.year + 1))
        )
        start_date = pd.Timestamp(f"{start_year}-{datetime.strptime(start_month, '%B').month:02d}-01")
        end_date = pd.Timestamp(f"{end_year}-{datetime.strptime(end_month, '%B').month:02d}-01")
    elif frequency.lower() == "annually":
        start_year = st.selectbox(
            "Start Year",
            options=list(range(overall_min_date.year, overall_max_date.year + 1))
        )
        end_year = st.selectbox(
            "End Year",
            options=list(range(overall_min_date.year, overall_max_date.year + 1))
        )
        start_date = pd.Timestamp(f"{start_year}-01-01")
        end_date = pd.Timestamp(f"{end_year}-12-31")

    if start_date < overall_min_date or end_date > overall_max_date:
        st.error(f"Selected dates must be within the range {overall_min_date.date()} to {overall_max_date.date()}.")
        return

    file_options = {key: info["columns"] for key, info in date_ranges.items()}
    y_file = st.selectbox("Select File for Dependent Variable (Y)", options=list(file_options.keys()))
    y_variable = st.selectbox("Select Dependent Variable (Y)", options=file_options[y_file])

    x_variables = st.multiselect("Select Independent Variables (X)", options=[var for file_vars in file_options.values() for var in file_vars])

    if st.button("Submit Selections"):
        # Prepare data to write to JSON
        variable_data = {
            "model": model_type,
            "frequency": frequency,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "y": {
                "variable": y_variable,
                "file_name": y_file,
                "file_path": date_ranges[y_file]["file_path"],
                "date_column": date_ranges[y_file]["date_column"]
            },
            "x": [
                {
                    "variable": x,
                    "file_name": next(file for file, vars in file_options.items() if x in vars),
                    "file_path": date_ranges[next(file for file, vars in file_options.items() if x in vars)]["file_path"],
                    "date_column": date_ranges[next(file for file, vars in file_options.items() if x in vars)]["date_column"]
                }
                for x in x_variables
            ]
        }

        # Write to JSON file
        output_file = "econometric_data/selected_variables.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(variable_data, f, indent=4)

        # Display success message and the written JSON
        st.success("Selections saved successfully!")
        st.json(variable_data)
