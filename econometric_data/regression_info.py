# regressly/econometric_data/regression_info.py

import streamlit as st


# Regression information dictionary
regression_info = {
    "Linear Regression": {
        "description": "Linear Regression is a statistical method for modeling the relationship between a dependent variable (Y) and one or more independent variables (X). It assumes a linear relationship between the variables.",
        "formula": "y = β0 + β1X1 + β2X2 + ... + ε",
        "input": "X values (features), Y value (continuous)",
        "output": "Predicted continuous value",
        "assumptions": [
            "Linear relationship between independent and dependent variables",
            "Homoscedasticity (constant variance of errors)",
            "Independence of errors",
            "Normally distributed errors"
        ],
        "practical_applications": [
            "Predicting house prices based on features like size, location, etc.",
            "Forecasting sales revenue based on advertising spend",
            "Modeling the effect of education on income"
        ],
        "key_concept": "Predicts a continuous outcome based on a linear combination of inputs."
    },
    "Logistic Regression": {
        "description": "Logistic Regression is used for binary classification problems where the outcome is either 0 or 1. It predicts the probability of a binary event occurring by modeling the log-odds of the outcome as a linear combination of the inputs.",
        "formula": "p = 1 / (1 + e^-(β0 + ∑βiXi))",
        "input": "X values (features), Y value (binary: 0/1)",
        "output": "Predicted probability between 0 and 1",
        "assumptions": [
            "The dependent variable is binary",
            "No multicollinearity among independent variables",
            "Linear relationship between independent variables and the log-odds of the dependent variable",
            "Large sample size is preferred"
        ],
        "practical_applications": [
            "Spam detection in emails (spam or not spam)",
            "Customer churn prediction (will the customer leave or stay)",
            "Disease diagnosis (positive or negative result)"
        ],
        "key_concept": "Predicts probability for binary classification."
    },
    "ARIMA": {
        "description": "ARIMA (AutoRegressive Integrated Moving Average) is a popular model for time series forecasting. It captures trends, seasonality, and noise in time-dependent data.",
        "formula": "Yt = c + ∑ϕiYt-i + ∑θjεt-j + εt",
        "input": "Time-indexed series of values, optional exogenous variables (X)",
        "output": "Predicted future values in the time series",
        "assumptions": [
            "The time series is stationary (mean, variance, and covariance are constant over time)",
            "No autocorrelation in residuals",
            "Appropriate differencing is applied to achieve stationarity"
        ],
        "practical_applications": [
            "Forecasting stock prices",
            "Predicting future sales based on historical data",
            "Modeling economic indicators such as GDP growth"
        ],
        "key_concept": "Time series forecasting."
    },
    "Probit Model": {
        "description": "The Probit model is a binary classification model that uses the normal cumulative distribution function (CDF) to model the probability of a binary outcome.",
        "formula": "P(y=1) = Φ(β0 + ∑βiXi)",
        "input": "X values (features), Y value (binary: 0/1)",
        "output": "Predicted probability between 0 and 1",
        "assumptions": [
            "The dependent variable is binary",
            "The error term follows a standard normal distribution"
        ],
        "practical_applications": [
            "Credit risk assessment (default or no default)",
            "Election outcome prediction (win or lose)",
            "Medical diagnosis (disease present or absent)"
        ],
        "key_concept": "Uses the normal distribution to model binary outcomes."
    },
    "Lasso Regression": {
        "description": "Lasso Regression (Least Absolute Shrinkage and Selection Operator) is a linear regression model that includes L1 regularization to reduce overfitting and perform automatic feature selection by shrinking some coefficients to zero.",
        "formula": "Loss = Σ(yᵢ - (β0 + ΣβⱼXⱼ))² + λΣ|βⱼ|",
        "input": "X values (features), Y value (continuous)",
        "output": "Predicted continuous value, with some coefficients potentially set to zero",
        "assumptions": [
            "Linear relationship between independent and dependent variables",
            "Features should not be highly correlated",
            "Errors should be normally distributed"
        ],
        "practical_applications": [
            "Predicting house prices with a large number of features",
            "Feature selection in high-dimensional datasets",
            "Modeling the effect of customer behavior on purchase amounts"
        ],
        "key_concept": "Reduces overfitting and performs feature selection by shrinking some coefficients to zero."
    },
    "Random Forest Classification": {
        "description": "Random Forest Classification is an ensemble learning method used for classifying categorical Y variables by building multiple decision trees and combining their predictions through majority vote.",
        "formula": "Prediction = Majority Vote (Classification Trees)",
        "input": "X values (features), Y value (categorical)",
        "output": "Predicted class label",
        "assumptions": [
            "Y variable must be categorical",
            "The trees are independent and diverse",
            "Handles both continuous and categorical features"
        ],
        "practical_applications": [
            "Spam detection",
            "Customer churn prediction",
            "Disease diagnosis",
            "Multi-class classification problems"
        ],
        "key_concept": "Predicts a class label by majority vote from decision trees."
    },
    "Random Forest Regression": {
        "description": "Random Forest Regression is an ensemble learning method used to predict continuous Y variables by averaging the predictions of multiple decision trees.",
        "formula": "Prediction = Average(Regression Trees)",
        "input": "X values (features), Y value (continuous)",
        "output": "Predicted continuous value",
        "assumptions": [
            "Y variable must be continuous",
            "The trees are independent and diverse",
            "Handles both continuous and categorical features"
        ],
        "practical_applications": [
            "House price prediction",
            "Sales forecasting",
            "Stock price prediction",
            "Credit scoring and risk assessment"
        ],
        "key_concept": "Predicts a continuous value by averaging the predictions from multiple decision trees."
    }
}

# ---- Function to Display Regression Info ----
def display_regression_info(model_name):
    """
    Displays detailed information about the selected regression model in Streamlit.
    """
    info = regression_info.get(model_name, {})
    if info:
        # Display model name
        st.markdown(f"<h3 style='color: #1E90FF;'>{model_name}</h3>", unsafe_allow_html=True)
        
        # Display description
        st.markdown(f"**Description:** {info['description']}")
        
        # Display formula
        st.markdown(f"**Formula:** `{info['formula']}`")
        
        # Display input and output
        st.markdown(f"**Input:** {info['input']}")
        st.markdown(f"**Output:** {info['output']}")
        
        # Display assumptions
        st.markdown("**Assumptions:**")
        st.markdown("  \n".join([f"- {assumption}" for assumption in info['assumptions']]))
        
        # Display practical applications
        st.markdown("**Practical Applications:**")
        st.markdown("  \n".join([f"- {app}" for app in info['practical_applications']]))
        
        # Display key concept
        st.markdown(f"**Key Concept:** {info['key_concept']}")
    else:
        st.error("Model information not found.")
