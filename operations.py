import streamlit as st
import pandas as pd
import numpy as np
import pickle
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from numpy.polynomial.polynomial import Polynomial

# Define preprocessing functions from the Jupyter notebook
def crop_spectrum(wavelengths, intensities, region=(400, 1800)):
    mask = (wavelengths >= region[0]) & (wavelengths <= region[1])
    return wavelengths[mask], intensities[mask]

def whitaker_hayes_despike(intensities, threshold=3):
    mean_intensity = np.mean(intensities)
    std_intensity = np.std(intensities)
    spikes = np.abs(intensities - mean_intensity) > threshold * std_intensity
    corrected_intensities = intensities.copy()
    corrected_intensities[spikes] = mean_intensity
    return corrected_intensities

def savgol_denoise(intensities, window_length=9, polyorder=3):
    return savgol_filter(intensities, window_length, polyorder)

def aspls_baseline(intensities, lam=1e5, p=0.01):
    L = len(intensities)
    D = csc_matrix(np.diff(np.eye(L), 2))
    I = csc_matrix(np.eye(L))
    w = np.ones(L)
    DTD = D.T @ D
    for i in range(10):
        W = spsolve(I + lam * DTD, w[:L-2] * intensities[:L-2])
        w = p * (intensities[:L-2] > W) + (1-p) * (intensities[:L-2] <= W)
    W = W.flatten()
    last_two_intensities = intensities[-2:].reshape(-1, 1).flatten()
    baseline_corrected_intensities = np.concatenate([W, last_two_intensities])
    return baseline_corrected_intensities

def polynomial_baseline_correction(wavelengths, intensities, degree=3):
    p = Polynomial.fit(wavelengths, intensities, deg=degree)
    baseline = p(wavelengths)
    corrected = intensities - baseline
    return corrected

def min_max_normalise(intensities):
    scaler = MinMaxScaler()
    intensities_2d = intensities.reshape(-1, 1)
    normalized_intensities = scaler.fit_transform(intensities_2d).flatten()
    return normalized_intensities

def preprocess_data(df):
    wavelengths, intensities = df['wavelength'], df['intensity']
    processed_df = preprocess_pipeline(wavelengths.values, intensities.values)
    intensities_processed = processed_df['intensity'].values
    
    if len(intensities_processed) != 1401:
        intensities_processed = np.resize(intensities_processed, 1401)
    
    return intensities_processed

def preprocess_pipeline(wavelengths, intensities):
    wavelengths, intensities = crop_spectrum(wavelengths, intensities)
    intensities = whitaker_hayes_despike(intensities)
    intensities = savgol_denoise(intensities)
    intensities = polynomial_baseline_correction(wavelengths, intensities)
    intensities = min_max_normalise(intensities)
    return pd.DataFrame({'wavelength': wavelengths, 'intensity': intensities})

# Function to load the model
def load_model(filename='model.pkl'):
    try:
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None


