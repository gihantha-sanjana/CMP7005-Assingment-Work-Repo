import streamlit as st
import pandas as pd



# Set the title of the app
st.title("Air Quality Prediction Dashboard")

url ="https://raw.githubusercontent.com/gihantha-sanjana/CMP7005-Assingment-Work-Repo/refs/heads/main/DataSet/Preprocessed-Data.csv?token=GHSAT0AAAAAAC4D6ORL6CNPKJPRLDFAO5K2Z3DYYHA"

# Sidebar to upload the dataset
st.sidebar.header("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

# Load the dataset from GitHub
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Load and display the dataset
try:
    data = load_data(url)
    st.subheader("Dataset Preview")
    st.write(data.head())

    # Show additional details
    st.subheader("Dataset Info")
    st.write(f"Shape: {data.shape}")
    st.write("Columns:", list(data.columns))
    st.write("Missing Values:")
    st.write(data.isna().sum())
except Exception as e:
    st.error(f"Error loading dataset: {e}")