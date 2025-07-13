import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Missing Data Visualizer", layout="wide")

st.title("🧼 Missing Data Analysis Dashboard")

# === Try to load local file if no upload ===
default_path = "customers-100.csv"

uploaded_file = st.file_uploader("Upload your CSV file (optional)", type=["csv"])

if uploaded_file:
    datasets = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
elif os.path.exists(default_path):
    datasets = pd.read_csv(default_path)
    st.warning(f"📂 Loaded default file from: `{default_path}`")
else:
    datasets = None
    st.info("👈 Please upload a CSV file or check local path.")

# === Continue if data is available ===
if datasets is not None:
    st.subheader("Preview of Dataset")
    st.dataframe(datasets.head(5))

    st.markdown("---")
    st.subheader("📊 Dataset Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", datasets.shape[0])
    with col2:
        st.metric("Total Columns", datasets.shape[1])

    total_missing = datasets.isnull().sum().sum()
    percent_missing = (total_missing / (datasets.shape[0] * datasets.shape[1])) * 100

    st.write(f"**🔎 Total Missing Values:** {total_missing}")
    st.write(f"**📉 Overall Missing Data (%):** {percent_missing:.2f}%")

    st.markdown("---")
    st.subheader("📌 Column-wise Missing Data (%)")
    col_missing = (datasets.isnull().sum() / datasets.shape[0]) * 100
    st.dataframe(col_missing[col_missing > 0].round(2).to_frame(name="% Missing"))

    st.markdown("---")
    st.subheader("📊 Heatmap of Missing Data")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(datasets.isnull(), cbar=False, cmap="Reds", yticklabels=False)
    st.pyplot(fig)
