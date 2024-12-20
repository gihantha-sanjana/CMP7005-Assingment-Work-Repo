# Import Packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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


st.sidebar.button("Prediction", type="primary")

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

