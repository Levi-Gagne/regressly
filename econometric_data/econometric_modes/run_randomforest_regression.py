# regressly/econometric_data/econometric_modes/run_randomforest_regression.py

import pandas as pd
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def load_and_prepare_rf_regression_data():
    """
    Load and prepare the Random Forest Regression data from the selected_variables.json file.
    """
    # Load the selected variables from the JSON file
    with open('econometric_data/selected_variables.json', 'r') as f:
        selected_data = json.load(f)

    # Load the dataset
    file_path = selected_data["y"]["file_path"]
    df = pd.read_csv(file_path)

    # Dependent variable (Y)
    y_variable = selected_data["y"]["variable"]
    y_data = df[y_variable]

    # Initialize DataFrame for X variables
    x_data = pd.DataFrame()

    # Process X variables
    for x_var in selected_data["x"]:
        x_column = x_var["variable"]

        if x_var["type"] == "categorical":
            # One-hot encoding for categorical variables
            encoder = OneHotEncoder(drop="first", sparse_output=False)
            encoded_columns = encoder.fit_transform(df[[x_column]])
            encoded_df = pd.DataFrame(encoded_columns, columns=encoder.get_feature_names_out([x_column]))
            x_data = pd.concat([x_data, encoded_df], axis=1)
        else:
            # Continuous variables
            x_data[x_column] = df[x_column]

    # Drop rows with missing values
    combined_data = pd.concat([y_data, x_data], axis=1).dropna()

    # Separate Y and X after alignment
    y_data = combined_data[y_variable]
    x_data = combined_data.drop(columns=[y_variable])

    # Get n_estimators from JSON
    n_estimators = selected_data["parameters"]["n_estimators"]

    return y_data, x_data, n_estimators


def display_run_regression():
    """
    Run and display the Random Forest Regression in Streamlit.
    """
    st.header("Random Forest Regression")

    if st.button("Run Regression"):
        try:
            # Load and prepare the data
            y_data, x_data, n_estimators = load_and_prepare_rf_regression_data()

            st.write("### Model Inputs:")
            st.write(f"- **Dependent Variable (Y):** {y_data.name}")
            st.write(f"- **Independent Variables (X):** {', '.join(x_data.columns)}")
            st.write(f"- **Number of Trees (n_estimators):** {n_estimators}")

            # Create and fit the Random Forest Regressor
            rf_regressor = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
            rf_regressor.fit(x_data, y_data)

            # Make predictions
            y_pred = rf_regressor.predict(x_data)

            # Calculate metrics
            mse = mean_squared_error(y_data, y_pred)
            r2 = r2_score(y_data, y_pred)

            st.subheader("Results")
            st.write(f"- **Mean Squared Error (MSE):** {mse:.2f}")
            st.write(f"- **R² Score:** {r2:.2f}")

            # Plot actual vs predicted values
            st.subheader("Actual vs Predicted")
            plot_actual_vs_predicted(y_data, y_pred)

            # Plot feature importances
            st.subheader("Feature Importances")
            plot_feature_importances(rf_regressor, x_data)

        except Exception as e:
            st.error(f"An error occurred: {e}")


def plot_actual_vs_predicted(y_data, y_pred):
    """
    Plot the actual vs predicted values for Random Forest Regression.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_data, y_pred, alpha=0.6, label="Predicted Values", color="#FFA07A")
    plt.plot(y_data, y_data, color="red", linewidth=2, label="Perfect Prediction Line")
    plt.title("Random Forest Regression: Actual vs Predicted Values")
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    plt.close()


def plot_feature_importances(model, x_data):
    """
    Plot the feature importances from the Random Forest model.
    """
    importances = model.feature_importances_
    features = x_data.columns
    importance_df = pd.DataFrame({"Feature": features, "Importance": importances})
    importance_df = importance_df.sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(importance_df["Feature"], importance_df["Importance"], color="#1E90FF")
    plt.title("Random Forest: Feature Importances")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.gca().invert_yaxis()
    plt.grid(True)
    st.pyplot(plt)
    plt.close()
