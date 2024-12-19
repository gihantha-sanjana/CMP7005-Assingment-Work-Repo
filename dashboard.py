pip install joblib
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
@st.cache
def load_model():
    model = joblib.load("random_forest_model.pkl")
    return model

model = load_model()

# Streamlit UI
st.title("Air Quality Prediction App")
st.write("Upload your dataset to predict MAX_AQI values.")

# Upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the uploaded CSV file
    input_data = pd.read_csv(uploaded_file, parse_dates=True, index_col=0)
    
    st.write("Uploaded Dataset:")
    st.dataframe(input_data.head())
    
    # Ensure input_data is preprocessed properly
    st.write("Preprocessing data...")

    # Create lag features (example for lag 3)
    lags = 3
    for i in range(1, lags + 1):
        input_data[f"lag_{i}"] = input_data['MAX_AQI'].shift(i)

    # Drop rows with missing values
    input_data = input_data.dropna()
    
    # Predict using the model
    if not input_data.empty:
        predictions = model.predict(input_data.drop('MAX_AQI', axis=1))
        input_data['Predicted_MAX_AQI'] = predictions
        
        st.write("Predictions:")
        st.dataframe(input_data[['Predicted_MAX_AQI']].head())

        # Download predictions as a CSV
        st.download_button(
            label="Download Predictions as CSV",
            data=input_data.to_csv().encode('utf-8'),
            file_name='predictions.csv',
            mime='text/csv'
        )
    else:
        st.write("Not enough data for prediction after preprocessing.")
