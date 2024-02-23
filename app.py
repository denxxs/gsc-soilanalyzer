import streamlit as st
import pandas as pd
import numpy as np
import pickle
from weather import weather_fetch
from streamlit_geolocation import streamlit_geolocation
import os
import psycopg2
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the connection string from the environment variable
connection_string = os.getenv('DATABASE_URL')

# Connect to the Postgres database
conn = psycopg2.connect(connection_string)

# Create a cursor object
cur = conn.cursor()

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# Initialize session state for user login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Function to check if user exists in the database
def user_exists(username):
    cur.execute("SELECT * FROM auth WHERE usern = %s", (username,))
    return cur.fetchone() is not None

# Function to insert new user into the database
def insert_user(username, password):
    cur.execute("INSERT INTO auth (usern, passw) VALUES (%s, %s)", (username, password))
    conn.commit()

# Function to verify user credentials
def verify_credentials(username, password):
    cur.execute("SELECT * FROM auth WHERE usern = %s AND passw = %s", (username, password))
    return cur.fetchone() is not None

# Function to get the most recent NPK values for a user
def get_recent_npk(username):
    cur.execute("""
    SELECT nrat, prat, krat, tem, mois 
    FROM npk 
    WHERE usern = %s 
    ORDER BY timel DESC 
    LIMIT 1;
    """, (username,))
    return cur.fetchone()

# Sidebar for Account Creation and Login
with st.sidebar:
    st.header("Account Management")
    if not st.session_state['logged_in']:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button('Create Account'):
            if user_exists(username):
                st.error("Username already taken.")
            else:
                insert_user(username, password)
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Account Created Successfully!")

        if st.button('Login'):
            if verify_credentials(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Logged in Successfully!")
            else:
                st.error("Invalid Credentials")
    else:
        st.success(f"You are logged in as {st.session_state['username']}")
        if st.button('Logout'):
            st.session_state['logged_in'] = False

# Main Page Content
if st.session_state['logged_in']:
    # Retrieve the most recent NPK values for the logged-in user
    npk_values = get_recent_npk(st.session_state['username'])
    
    # Check if we got the values back from the database
    if npk_values:
        nrat, prat, krat, tem, mois = npk_values
    else:
        st.error("Could not retrieve soil data for the user.")
        nrat, prat, krat, tem, mois = 83, 45, 60, 28, 70  # Default values in case of error

    # Define initial soil data with values retrieved from the database
    soil_data = {
        'N': [nrat],
        'P': [prat],
        'K': [krat],
        'Temperature (°C)': [tem],
        'Humidity': [mois],
        'pH Level': [7.0],  # Default value, adjust as needed
        'rainfall(mm)': [150.9],  # Default value, adjust as needed
        'lat': [0],
        'long': [0]
    }
    soil_df = pd.DataFrame(soil_data)

    # Making crop recommendation
    def predict_crop(new_Ni, new_Pho, new_Ki, new_temperature, new_humidity, new_ph_level, new_rainfall):
        # Load the model from the .pkl file
        with open('models/RandomForest.pkl', 'rb') as file:
            model = pickle.load(file)

        soil_dataValue = np.array([[new_Ni, new_Pho, new_Ki, new_temperature, new_humidity, new_ph_level, new_rainfall]])
        probabilities = model.predict_proba(soil_dataValue)
        top_5_indices = np.argsort(probabilities, axis=1)[:, ::-1][:, :5]
        top_5_crops = model.classes_[top_5_indices]
        return top_5_crops.flatten()
    
    # Columns for the soil type image and the two sections on the right
    col1, col2 = st.columns([2, 4])

    # Soil type image placeholder
    with col1:
        st.header("Soil Type")
        st.image("static/soil.png", use_column_width=True, output_format='auto')  # Replace with your image path

    with col2:
        # Editable Soil Data
        st.header("Editable Soil Data")
        # Creating columns for each soil parameter input
        col_N, col_P, col_K, col_temp, col_mois, col_ph, col_rain = st.columns(7)

        with col_N:
            new_N = st.number_input("Nitrogen (N)", value=nrat)
        with col_P:
            new_P = st.number_input("Phosphorus (P)", value=prat)
        with col_K:
            new_K = st.number_input("Potassium (K)", value=krat)
        with col_temp:
            new_temp = st.number_input("Temperature (°C)", value=tem)
        with col_mois:
            new_mois = st.number_input("Moisture (%)", value=mois)
        with col_ph:
            new_ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0)
        with col_rain:
            new_rain = st.number_input("Rainfall (mm)", value=150.9)  # Replace with real default if needed

        # Update button
        if st.button('Update Soil Data'):
            soil_df.loc[0, 'N'] = new_N
            soil_df.loc[0, 'P'] = new_P
            soil_df.loc[0, 'K'] = new_K
            soil_df.loc[0, 'Temperature (°C)'] = new_temp
            soil_df.loc[0, 'Humidity'] = new_mois
            soil_df.loc[0, 'pH Level'] = new_ph
            soil_df.loc[0, 'rainfall(mm)'] = new_rain
            st.write("Updated Soil Data:")
            st.write(soil_df)

        # Crop recommendation section
        if st.button('Predict Best Crops'):
            top_crops = predict_crop(new_N, new_P, new_K, new_temp, new_mois, new_ph, new_rain)
            st.subheader("Top Crop Recommendations:")
            for crop in top_crops:
                st.write(f"- {crop}")

else:
    st.warning("Please create an account or login to access the features.")
