import streamlit as st
import joblib

# Title of the Streamlit App
st.title("Load and Use a .pkl File in Streamlit")

# Sidebar input to upload or load the file
st.sidebar.title("Model Options")

# Option to upload a .pkl file
uploaded_file = st.sidebar.file_uploader("Upload your model (.pkl file)", type=["pkl"])

# Load the .pkl file
if uploaded_file is not None:
    # Display file name
    st.write(f"Loaded file: {uploaded_file.name}")
    
    # Load the model using joblib
    try:
        model = joblib.load(uploaded_file)
        st.success("Model loaded successfully!")
        
        # Example: Use the loaded model (assumes a regression model)
        sample_input = st.text_input("Enter a sample input for prediction (comma-separated values):")
        
        if st.button("Predict"):
            try:
                input_values = [float(x) for x in sample_input.split(",")]
                prediction = model.predict([input_values])
                st.write(f"Prediction: {prediction[0]}")
            except Exception as e:
                st.error(f"Error making prediction: {e}")
    
    except Exception as e:
        st.error(f"Failed to load model: {e}")
else:
    st.warning("Please upload a .pkl file to proceed.")
