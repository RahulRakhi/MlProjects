import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Set page config (must be first Streamlit call)
st.set_page_config(page_title="Marks Predictor", layout="centered")

# App title
st.title("📘 Marks Predictor")
st.write("This app predicts your marks based on hours studied using your own data.")

# --- Load your CSV data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("marks.csv")  # File should have 'hrs' and 'marks' columns
        return df
    except FileNotFoundError:
        st.error("❌ File 'marks.csv' not found. Please place it in the same folder as this script.")
        return None

data = load_data()

# Proceed only if data is loaded
if data is not None:
    # Show the dataset
    st.subheader("📂 Training Data")
    st.dataframe(data)

    # Train model
    X = data[['hrs']]
    y = data['marks']
    model = LinearRegression()
    model.fit(X, y)

    # Take user input
    hours = st.slider("⏱️ Enter Hours Studied", 0.0, 12.0, step=0.5)
    predicted_marks = model.predict([[hours]])[0]

    # Show result
    st.subheader("📊 Predicted Marks")
    st.success(f"Based on {hours} hours of study, you may score: **{predicted_marks:.2f} / 100**")

    # Show model formula
    st.info(f"**Model Equation:** Marks = {model.coef_[0]:.2f} × Hours + {model.intercept_:.2f}")
