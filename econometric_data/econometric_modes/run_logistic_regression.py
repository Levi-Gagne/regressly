# regressly/econometric_data/econometric_modes/run_logistic_regression.py

import pandas as pd
import json
import statsmodels.api as sm
import streamlit as st
import matplotlib.pyplot as plt


def load_and_prepare_logistic_data():
    """
    Load and prepare the logistic regression data from the selected_variables.json file.
    """
    # Load selected variables from the JSON file
    with open('econometric_data/selected_variables.json', 'r') as f:
        selected_data = json.load(f)

    # Load the CSV file once
    file_path = selected_data["y"]["file_path"]
    df = pd.read_csv(file_path)

    # Load the dependent variable (Y)
    y_variable = selected_data["y"]["variable"]
    y_data = df[y_variable].astype(int)  # Ensure binary target is numeric

    # Initialize a DataFrame for X variables
    x_data = pd.DataFrame()

    # Process independent variables (X)
    for x_var in selected_data["x"]:
        x_column = x_var["variable"]

        if x_var["type"] == "categorical":
            # Binary or one-hot encoding for categorical columns
            unique_values = df[x_column].unique()
            if len(unique_values) == 2:
                mapping = {unique_values[0]: 0, unique_values[1]: 1}
                x_data[x_column] = df[x_column].map(mapping)
            else:
                x_encoded = pd.get_dummies(df[x_column], prefix=x_column, drop_first=True)
                x_data = pd.concat([x_data, x_encoded], axis=1)
        else:
            x_data[x_column] = df[x_column]

    # Drop rows with missing values
    combined_data = pd.concat([y_data, x_data], axis=1).dropna()

    # Separate Y and X after alignment
    y_data = combined_data[y_variable]
    x_data = combined_data.drop(columns=[y_variable])

    return y_data, x_data


def display_run_regression():
    """
    Run the logistic regression and display results in Streamlit.
    """
    if st.button("Run Logistic Regression"):
        # Load and prepare data
        y_data, x_data = load_and_prepare_logistic_data()

        # Add a constant for the intercept
        x_data = sm.add_constant(x_data)

        # Run the logistic regression
        logit_model = sm.Logit(y_data, x_data).fit()

        # Display the summary
        st.subheader("Logistic Regression Results")
        st.text(logit_model.summary())

        # Plot the predicted probabilities
        y_pred_prob = logit_model.predict(x_data)
        plot_logistic_regression_results(y_pred_prob)


def plot_logistic_regression_results(y_pred_prob):
    """
    Plot the predicted probabilities for logistic regression.
    """
    st.subheader("Predicted Probabilities Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(y_pred_prob, bins=20, edgecolor='black', alpha=0.7)
    ax.axvline(0.5, color='red', linestyle='--', label="Threshold (0.5)")
    ax.set_title("Logistic Regression: Predicted Probabilities")
    ax.set_xlabel("Predicted Probability")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)