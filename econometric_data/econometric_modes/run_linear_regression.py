# regressly/econometric_data/econometric_modes/run_linear_regression.py

import pandas as pd
import json
import statsmodels.api as sm
import streamlit as st
import altair as alt

def load_and_prepare_linear_data():
    """
    Load and prepare the data for linear regression from the selected_variables.json file.
    """
    with open('econometric_data/selected_variables.json', 'r') as f:
        selected_data = json.load(f)

    y_variable = selected_data["y"]["variable"]
    y_file_path = selected_data["y"]["file_path"]

    y_df = pd.read_csv(y_file_path, parse_dates=[selected_data["y"]["date_column"]])
    y_df.set_index(selected_data["y"]["date_column"], inplace=True)
    y_data = y_df[y_variable]

    x_data = pd.DataFrame(index=y_data.index)
    for x_var in selected_data["x"]:
        x_variable = x_var["variable"]
        x_file_path = x_var["file_path"]

        x_df = pd.read_csv(x_file_path, parse_dates=[x_var["date_column"]])
        x_df.set_index(x_var["date_column"], inplace=True)
        x_data[x_variable] = x_df[x_variable]

    combined_data = pd.concat([y_data, x_data], axis=1).dropna()

    y_data = combined_data[y_variable]
    x_data = combined_data.drop(columns=[y_variable])

    return y_data, x_data, y_variable, [x["variable"] for x in selected_data["x"]]

def plot_regression_results_with_streamlit(y_data, y_pred):
    """
    Plot the actual vs. predicted values using Streamlit's Altair integration.
    """
    data = pd.DataFrame({
        "Actual": y_data,
        "Predicted": y_pred
    })

    chart = alt.Chart(data).mark_circle(size=60, color="#FFA07A").encode(
        x=alt.X("Actual", title="Actual Values"),
        y=alt.Y("Predicted", title="Predicted Values"),
        tooltip=["Actual", "Predicted"]
    ).interactive()

    line = alt.Chart(data).mark_line(color="red", strokeWidth=2).encode(
        x="Actual",
        y="Actual"
    )

    st.altair_chart(chart + line, use_container_width=True)

def format_regression_results(model, y_variable, x_variable_names):
    """
    Format and display regression results in Streamlit.
    """
    st.markdown("<h2 style='color: #4CAF50;'>OLS Regression Results</h2>", unsafe_allow_html=True)
    st.markdown(f"<b>Dependent Variable:</b> <span style='color: #FF5733;'>{y_variable}</span>", unsafe_allow_html=True)
    st.markdown(f"<b>Independent Variables:</b> <span style='color: #1E90FF;'>{', '.join(x_variable_names)}</span>", unsafe_allow_html=True)

    st.markdown("### Model Summary")
    st.text(model.summary())

    st.markdown("### Coefficients")
    results_df = pd.DataFrame({
        "Variable": model.params.index,
        "Coefficient": model.params.values,
        "Standard Error": model.bse.values,
        "t-Statistic": model.tvalues.values,
        "P-Value": model.pvalues.values,
    })
    st.dataframe(results_df)

def run_model():
    """
    Run the linear regression using the prepared data and display results.
    """
    y_data, x_data, y_variable, x_variable_names = load_and_prepare_linear_data()
    x_data = sm.add_constant(x_data)
    linear_model = sm.OLS(y_data, x_data).fit()

    format_regression_results(linear_model, y_variable, x_variable_names)
    st.markdown("### Regression Plot")
    plot_regression_results_with_streamlit(y_data, linear_model.predict(x_data))

def display_run_regression():
    """
    Display the "Run Regression" button and run linear regression when clicked.
    """
    st.header("Run Linear Regression")

    if st.button("Run Regression"):
        try:
            run_model()
        except Exception as e:
            st.error(f"An error occurred while running the regression: {e}")
