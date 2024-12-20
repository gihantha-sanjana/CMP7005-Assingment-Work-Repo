# Import Packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from io import BytesIO
import requests
# import joblib
import os
# from sklearn.preprocessing import MinMaxScaler
import numpy as np
import streamlit as st
import pandas as pd
import pickle

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar with image
st.sidebar.header('Air Quality Prediction App')
st.sidebar.image(
    "/workspaces/CMP7005-Assingment-Work-Repo/Air-Quality-Improvement-through-WtE.jpeg",  # Replace with your image file path
    use_column_width=True
)

url = "https://raw.githubusercontent.com/gihantha-sanjana/CMP7005-Assingment-Work-Repo/refs/heads/main/Preprocessed-Data.csv"

# Load the dataset from GitHub
@st.cache_data
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Load dataset from URL and display basic info
data = load_data(url)
if data is not None:
    st.subheader("Dataset Preview")
    st.write(data.head())

# Convert DATETIME column to pandas datetime (if not already done)
data["DATETIME"] = pd.to_datetime(data["DATETIME"])
    

# Sidebar filters
# Select station
st.sidebar.subheader('Select Station')
station_names = data['STATION'].unique()
selected_station = st.sidebar.selectbox('Choose Station', station_names)

# Select air quality category
st.sidebar.subheader('Select Air Quality Category')
unique_air_quality_categories = data['AQI_CATEGORY'].unique()
selected_air_category = st.sidebar.selectbox('Choose Air Quality Category', unique_air_quality_categories)

# Select date range
st.sidebar.subheader('Select Date Range')
min_date = data["DATETIME"].min()
max_date = data["DATETIME"].max()
start_date = st.sidebar.date_input("Start Date", min_date.date(), min_value=min_date.date(), max_value=max_date.date())
end_date = st.sidebar.date_input("End Date", max_date.date(), min_value=min_date.date(), max_value=max_date.date())

# Filter function
def filter_data(data, station, air_category, start_date, end_date):
    # Apply filters
    filtered = data[
        (data["STATION"] == station) &
        (data["AQI_CATEGORY"] == air_category) &
        (data["DATETIME"].dt.date >= pd.to_datetime(start_date).date()) &
        (data["DATETIME"].dt.date <= pd.to_datetime(end_date).date())
    ]
    return filtered

# Apply filters to the dataset
filtered_data = filter_data(data, selected_station, selected_air_category, start_date, end_date)

# Display filtered dataset
st.subheader(f"Filtered Data for Station '{selected_station}' and Air Category '{selected_air_category}'")
st.write(f"Data from {start_date} to {end_date}:")
if not filtered_data.empty:
    st.dataframe(filtered_data)
else:
    st.warning("No data available for the selected filters.")

# Plot PM2.5 levels over time
if not filtered_data.empty:
    st.subheader(f"Time Series of Air Quality for '{selected_station}' in '{selected_air_category}' Category")
    
    # Plot PM2.5 over time
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_data["DATETIME"], filtered_data["PM2.5"], label="PM2.5", color='blue', marker='o')
    plt.xlabel("Date")
    plt.ylabel("PM2.5 Levels")
    plt.title(f"PM2.5 Levels Over Time ({start_date} to {end_date})")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)
else:
    st.warning("No data available to plot for the selected filters.")



# Prediction-------------------------------------
# st.subheader("Prediction Page")

# model_url = "https://github.com/gihantha-sanjana/CMP7005-Assingment-Work-Repo/raw/refs/heads/main/random_forest_model.pkl"
# data_path = "https://raw.githubusercontent.com/gihantha-sanjana/CMP7005-Assingment-Work-Repo/refs/heads/main/Preprocessed-Data.csv"

# @st.cache_resource
# def load_model_from_github(url):
#     response = requests.get(url)     
#     if response.status_code == 200:
#         model_file = BytesIO(response.content)
#         model = joblib.load(model_file)
#         return model
#     else:
#         st.error(f"Failed to fetch the model. HTTP status code: {response.status_code}")
#         return None
    
# @st.cache_resource
# def load_data_from_github(url):
#     response = requests.get(url)     
#     if response.status_code == 200:
#         data_path = BytesIO(response.content)
#         data = joblib.load(data_path)
#         return data
#     else:
#         st.error(f"Failed to fetch the model. HTTP status code: {response.status_code}")
#         return None

# # Load the model
# model = load_model_from_github(model_url)
# data = load_data_from_github(data_path)

# with open(model, 'rb') as file:
#     model = pickle.load(file)

# # Load dataset
# data = pd.read_csv(data_path)

# # Streamlit app
# st.title("Prediction App")

# st.header("Input Features")

# # Assuming the dataset has a specific set of features
# # Use the dataset column names to dynamically create input fields
# user_input = {}
# for col in data.columns:
#     if data[col].dtype == 'object':
#         user_input[col] = st.selectbox(f"{col}:", data[col].unique())
#     elif data[col].dtype in ['int64', 'float64']:
#         user_input[col] = st.number_input(f"{col}:", value=float(data[col].mean()))

# # Button to make predictions
# if st.button("Predict"):
#     # Prepare input for the model
#     input_df = pd.DataFrame([user_input])
#     prediction = model.predict(input_df)
    
#     st.subheader("Prediction Result:")
#     st.write(prediction[0])
# -----------------------------------------

