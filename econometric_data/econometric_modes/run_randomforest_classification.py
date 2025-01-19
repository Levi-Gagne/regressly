# regressly/econometric_data/econometric_modes/run_randomforest_classification.py


import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def load_and_prepare_rf_classification_data():
    """
    Load and prepare the Random Forest Classification data from the selected_variables.json file.
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


def display_run_classification():
    """
    Run and display the Random Forest Classification in Streamlit.
    """
    st.header("Random Forest Classification")

    if st.button("Run Classification"):
        try:
            # Load and prepare the data
            y_data, x_data, n_estimators = load_and_prepare_rf_classification_data()

            st.write("### Model Inputs:")
            st.write(f"- **Dependent Variable (Y):** {y_data.name}")
            st.write(f"- **Independent Variables (X):** {', '.join(x_data.columns)}")
            st.write(f"- **Number of Trees (n_estimators):** {n_estimators}")

            # Create and fit the Random Forest Classifier
            rf_classifier = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
            rf_classifier.fit(x_data, y_data)

            # Make predictions
            y_pred = rf_classifier.predict(x_data)

            # Calculate metrics
            accuracy = accuracy_score(y_data, y_pred)
            st.subheader("Results")
            st.write(f"- **Accuracy Score:** {accuracy:.2f}")
            st.text("Classification Report")
            st.text(classification_report(y_data, y_pred))

            # Plot confusion matrix
            st.subheader("Confusion Matrix")
            plot_confusion_matrix(y_data, y_pred)

            # Plot feature importances
            st.subheader("Feature Importances")
            plot_feature_importances(rf_classifier, x_data)

        except Exception as e:
            st.error(f"An error occurred: {e}")


def plot_confusion_matrix(y_data, y_pred):
    """
    Plot the confusion matrix.
    """
    cm = confusion_matrix(y_data, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=True, yticklabels=True)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
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
