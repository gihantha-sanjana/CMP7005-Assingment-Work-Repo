import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from streamlit_folium import folium_static



st.title("Air Quality Prediction Dashboard")

# Link DataSet
cleaned_df = pd.read_csv('https://raw.githubusercontent.com/gihantha-sanjana/CMP7005-Assingment-Work-Repo/refs/heads/main/DataSet/Preprocessed-Data.csv?token=GHSAT0AAAAAAC4D6ORKFZI5O7RCZKX2XU5MZ3DYPQQ')



# url =""

# Load the dataset from GitHub
@st.cache_data
def load_data(cleaned_df):
    return pd.read_csv(cleaned_df)

# Load and display the dataset
try:
    data = load_data(cleaned_df)
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


# st.dataframe(cleaned_df.head(10))