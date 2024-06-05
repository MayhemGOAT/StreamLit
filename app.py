import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

# Load your trained model
@st.cache(allow_output_mutation=True)
def load_model(model_path):
    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model

# Define the preprocessing functions
def crop_spectrum(wavelengths, intensities, region=(700, 1800)):
    mask = (wavelengths >= region[0]) & (wavelengths <= region[1])
    return wavelengths[mask], intensities[mask]

def whittaker_hayes_despike(intensities, threshold=3):
    return corrected_intensities

def aspls_baseline(intensities, lam=1e5, p=0.01):
    return intensities - W

def min_max_normalise(intensities):
    scaler = MinMaxScaler()
    return scaler.fit_transform(intensities.reshape(-1, 1)).flatten()

# Combine all preprocessing steps into a pipeline
def preprocess_pipeline(wavelengths, intensities):
    def preprocess_pipeline(wavelengths, intensities):
    # Convert wavelengths to numeric, handling non-numeric values
    wavelengths = pd.to_numeric(wavelengths, errors='coerce')
    if wavelengths.isna().any():
        wavelengths = wavelengths.fillna(method='ffill')  

    wavelengths, intensities = crop_spectrum(wavelengths, intensities)
    intensities = whittaker_hayes_despike(intensities)
    intensities = aspls_baseline(intensities)
    intensities = min_max_normalise(intensities)
    df = pd.DataFrame({'Raman Shift': wavelengths, 'intensity': intensities})
    return df

# Streamlit user interface
def main():
    st.title('Spectral Data Classifier')

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_file is not None:
        # Assuming that the CSV has no header row, specify the column names explicitly
        input_df = pd.read_csv(uploaded_file, names=['wavelength', 'intensity'])

        # Check if 'wavelength' and 'intensity' columns exist in the uploaded file
        if 'wavelength' not in input_df.columns or 'intensity' not in input_df.columns:
            st.error("CSV file does not contain required 'wavelength' or 'intensity' columns.")
            st.stop()
        
        # If the columns are present, process the data
        processed_data = preprocess_pipeline(input_df['wavelength'], input_df['intensity'])
        


# Run the main function
if __name__ == '__main__':
    main()
