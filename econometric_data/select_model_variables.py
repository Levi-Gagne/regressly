# regressly/select_model_variables.py

import json
import os
import importlib
import streamlit as st

import json
import os
import importlib
import streamlit as st

# Path to the JSON configuration file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(CURRENT_DIR, "date_and_model_selection.json")

def display_model_variables():
    """
    Dynamically load and display widgets for the selected regression model.
    """
    # Load the JSON file
    if not os.path.exists(JSON_FILE):
        st.error("❌ JSON file not found. Please complete Step 2 first.")
        return

    with open(JSON_FILE, 'r') as f:
        selection_data = json.load(f)

    model_type = selection_data.get("model", "").lower()

    try:
        # Dynamically load the correct module
        module_name = f"econometric_data.econometric_modes.{model_type.replace(' ', '_')}_model"
        module = importlib.import_module(module_name)
        module.display_widgets()
    except ImportError as e:
        st.error(f"❌ Error importing module: {e}")
    except AttributeError as e:
        st.error(f"❌ Error: Function not found in module: {e}")


def run_regression_model():
    """
    Dynamically load and run the selected regression model.
    """
    if not os.path.exists(JSON_FILE):
        st.error("❌ JSON file not found. Please complete Step 2 first.")
        return

    with open(JSON_FILE, 'r') as f:
        selection_data = json.load(f)

    model_type = selection_data.get("model", "").lower()

    try:
        # Dynamically load and run the correct regression module
        module_name = f"econometric_data.econometric_modes.run_{model_type.replace(' ', '_')}"
        module = importlib.import_module(module_name)
        module.run_model()
    except ImportError as e:
        st.error(f"❌ Error importing module: {e}")
    except AttributeError as e:
        st.error(f"❌ Error: Function not found in module: {e}")
