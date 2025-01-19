# regressly/app.py

import streamlit as st
import os
import json
from econometric_data.upload_file import streamlit_file_uploader
from econometric_data.model_date_selection import display_model_date_selection
from econometric_data.select_model_variables import display_model_variables
from econometric_data.econometric_modes.run_linear_regression import display_run_regression as run_linear
from econometric_data.econometric_modes.run_logistic_regression import display_run_regression as run_logistic

# Ensure the save directory exists (if required globally for the app)
SAVE_DIR = "uploaded_files"
os.makedirs(SAVE_DIR, exist_ok=True)

def main():
    # App Header
    st.components.v1.html("""
        <div style="text-align: center;">
            <h1 style="color: #4A90E2; font-size: 3.5em; font-weight: bold; margin-bottom: 0;">Regressly</h1>
        </div>
        <div style="text-align: left; margin-top: 10px;">
            <h3 style="color: #7BAFD4; font-size: 1.8em;">Simplifying Regression Analysis</h3>
        </div>
    """, height=120)

    # Navigation Menu
    st.sidebar.title("Navigation")
    options = [
        "Step 1: Upload CSV",
        "Step 2: Model & Date Selection",
        "Step 3: Configure Model Variables",
        "Step 4: Run Regression",
    ]
    choice = st.sidebar.radio("Select a Step", options)

    # Route the app to the appropriate module based on user selection
    if choice == "Step 1: Upload CSV":
        step1_upload_csv()
    elif choice == "Step 2: Model & Date Selection":
        step2_model_date_selection()
    elif choice == "Step 3: Configure Model Variables":
        step3_configure_model_variables()
    elif choice == "Step 4: Run Regression":
        step4_run_regression()

    # Footer
    st.components.v1.html("""
        <hr>
        <div style="text-align: center;">
            <p style="color: purple;">© 2025 LMG_Services. All rights reserved.</p>
        </div>
    """, height=40)

# Step 1: File Upload
def step1_upload_csv():
    """Delegate file upload functionality to the corresponding module."""
    streamlit_file_uploader()

# Step 2: Model & Date Selection
def step2_model_date_selection():
    """Delegate model and date selection to the corresponding module."""
    display_model_date_selection()

# Step 3: Configure Model Variables
def step3_configure_model_variables():
    """Delegate model variable configuration to the corresponding module."""
    display_model_variables()

# Step 4: Run Regression
def step4_run_regression():
    """Run the selected regression model."""
    json_file = "econometric_data/date_and_model_selection.json"
    if not os.path.exists(json_file):
        st.error("JSON configuration file not found. Complete Step 2 first.")
        return

    with open(json_file, 'r') as f:
        selection_data = json.load(f)

    model_type = selection_data.get("model", "").title()  # Capitalize the model type
    regression_title = f"Run {model_type}"  # Avoid repeating "Regression"
    st.subheader(regression_title)  # Dynamic title

    # Execute the correct regression
    if model_type.lower() == "linear regression":
        run_linear()
    elif model_type.lower() == "logistic regression":
        run_logistic()
    elif model_type.lower() == "lasso regression":
        from econometric_data.econometric_modes.run_lasso_regression import run_lasso_model
        if st.button("Run Lasso Regression"):
            run_lasso_model()
    else:
        st.error(f"Unsupported model type: {model_type}")

# Run the App
if __name__ == "__main__":
    main()
