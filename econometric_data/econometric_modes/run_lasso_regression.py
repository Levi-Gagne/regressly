# regressly/econometric_data/econometric_modes/run_lasso_regression.py

import os
import pandas as pd
import json
from sklearn.linear_model import Lasso
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import streamlit as st
import matplotlib.pyplot as plt

# Function to load and prepare the Lasso data
def load_and_prepare_lasso_data():
    """
    Load and prepare the Lasso regression data from the selected_variables.json file.
    """
    # Load the selected variables from the JSON file
    with open('econometric_data/selected_variables.json', 'r') as f:
        selected_data = json.load(f)

    # Load the CSV file once
    file_path = selected_data["y"]["file_path"]
    df = pd.read_csv(file_path)

    # Load the dependent variable (Y)
    y_variable = selected_data["y"]["variable"]
    y_data = df[y_variable]

    # Initialize a DataFrame for X variables
    x_data = pd.DataFrame()

    # Process independent variables (X)
    for x_var in selected_data["x"]:
        x_column = x_var["variable"]

        if x_var["type"] == "categorical":
            # Check the unique values in the categorical column
            unique_values = df[x_column].unique()

            if len(unique_values) == 2:
                # Binary encoding (0/1) for two unique values
                mapping = {unique_values[0]: 0, unique_values[1]: 1}
                x_data[x_column] = df[x_column].map(mapping)
            else:
                # One-hot encoding for more than two unique values
                encoder = OneHotEncoder(drop="first", sparse_output=False)
                x_encoded = pd.DataFrame(
                    encoder.fit_transform(df[[x_column]]),
                    columns=encoder.get_feature_names_out([x_column])
                )
                x_data = pd.concat([x_data, x_encoded], axis=1)
        else:
            # For continuous variables, add directly to the DataFrame
            x_data[x_column] = df[x_column]

    # Drop rows with missing values
    combined_data = pd.concat([y_data, x_data], axis=1).dropna()

    # Separate Y and X after alignment
    y_data = combined_data[y_variable]
    x_data = combined_data.drop(columns=[y_variable])

    # Get the alpha value from the JSON
    alpha_value = selected_data["alpha"]

    return y_data, x_data, alpha_value


# Function to run the Lasso regression
def run_lasso_model():
    """
    Run the Lasso regression using the prepared data.
    """
    # Load and prepare the data
    y_data, x_data, alpha_value = load_and_prepare_lasso_data()

    # Streamlit: Display summary of inputs
    st.write("### Running Lasso Regression")
    st.write(f"**Dependent Variable (Y):** {y_data.name}")
    st.write(f"**Independent Variables (X):** {', '.join(x_data.columns)}")
    st.write(f"**Alpha Value:** {alpha_value}")

    # Create and fit the Lasso Regression model
    lasso = Lasso(alpha=alpha_value)
    lasso.fit(x_data, y_data)

    # Make predictions
    y_pred = lasso.predict(x_data)

    # Calculate performance metrics
    mse = mean_squared_error(y_data, y_pred)
    r2 = r2_score(y_data, y_pred)

    # Streamlit: Display results
    st.write("### Results")
    st.write(f"- **Mean Squared Error (MSE):** {mse:.2f}")
    st.write(f"- **R² Score:** {r2:.2f}")

    # Display coefficients in a table
    coefficients_df = pd.DataFrame({
        "Feature": x_data.columns,
        "Coefficient": lasso.coef_
    }).sort_values(by="Coefficient", ascending=False)
    st.write("### Feature Coefficients")
    st.dataframe(coefficients_df)

    # Plot feature coefficients
    st.write("### Coefficient Plot")
    st.pyplot(plot_feature_coefficients(coefficients_df))

    # Plot actual vs predicted values
    st.write("### Actual vs Predicted Plot")
    st.pyplot(plot_lasso_regression_results(y_data, y_pred))


def plot_feature_coefficients(coefficients_df):
    """
    Plot the feature coefficients from the Lasso regression.
    """
    plt.figure(figsize=(10, 6))
    plt.barh(coefficients_df["Feature"], coefficients_df["Coefficient"], color="#1E90FF")
    plt.title("Lasso Regression: Feature Coefficients")
    plt.xlabel("Coefficient Value")
    plt.ylabel("Feature")
    plt.grid(True)
    return plt.gcf()


def plot_lasso_regression_results(y_data, y_pred):
    """
    Plot the actual vs predicted values for Lasso regression.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_data, y_pred, alpha=0.6, label="Predicted Values", color="#FFA07A")
    plt.plot(y_data, y_data, color="red", linewidth=2, label="Perfect Prediction Line")
    plt.title("Lasso Regression: Actual vs Predicted Values")
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.legend()
    plt.grid(True)
    return plt.gcf()