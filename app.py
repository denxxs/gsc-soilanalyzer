import streamlit as st
import pandas as pd
import numpy as np
import pickle
from weather import weather_fetch
from streamlit_geolocation import streamlit_geolocation
import os
from reverse_location import get_city_name
from test_visualcrossing import get_weather
from datetime import datetime # for testing ig -- get current time
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
        'place' : ['Chennai'],
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
        # Display editable DataFrame using st.columns()
        st.header("Editable Soil Data")

        # Columns for the soil data
        # location, Ni, Pho, Ki, temperature, humidity, ph_level, rainfall = st.columns(8)
        cord, Ni, Pho, Ki, ph_level, rainfall = st.columns(6)

        # N level
        with Ni:
            new_Ni = st.number_input("N", value=soil_df.loc[0, 'N'])

        # P level
        with Pho:
            new_Pho = st.number_input("P", value=soil_df.loc[0, 'P'])

        # K level
        with Ki:
            new_Ki = st.number_input("K", value=soil_df.loc[0, 'K'])

        # rainfall level
        with rainfall:
            new_rainfall = st.number_input("rainfall(mm)", value=soil_df.loc[0, 'rainfall(mm)'])
            
        # pH Level
        with ph_level:
            new_ph_level = st.number_input("pH Level", value=soil_df.loc[0, 'pH Level'])

        # # Humidity
        # with humidity:
        #     new_humidity = st.number_input("Humidity", value=soil_df.loc[0, 'Humidity'])

        # # Temperature
        # with temperature:
        #     new_temperature = st.number_input("Temperature (°C)", value=soil_df.loc[0, 'Temperature (°C)'])

        # location
        # with location:
        #     new_location = st.text_input("Location Name", value=soil_df.loc[0, 'location'])
        #     # update temp and humidity with weather_fetch
        #     new_temperature, new_humidity = weather_fetch(new_location)

        with cord :
            current_time = datetime.now()
            current_time = str(current_time)

            new_lat = 37.7749
            new_lon = -122.4194
            location = streamlit_geolocation()
            new_lat = location['latitude']
            new_lon = location['longitude']
            city = get_city_name(new_lat, new_lon)
            
            # if location['latitude'] and location['longitude']:
            #     new_temperature, new_humidity = get_weather(city, current_time)
            # else:
            #     new_temperature, new_humidity = get_weather(city, "2024-02-23 12:50:32.23")

            try:
                new_temperature, new_humidity, new_rainfall = get_weather(city, current_time)
            except:
                st.error("Please click on geolocation button/enable location services.")
                # Set default values
                new_temperature = 0.0
                new_humidity = 0.0
                new_rainfall = 0.0

        # Update the DataFrame with new values
        soil_df.loc[0, 'N'] = new_Ni
        soil_df.loc[0, 'P'] = new_Pho
        soil_df.loc[0, 'K'] = new_Ki
        soil_df.loc[0, 'Temperature (°C)'] = new_temperature
        soil_df.loc[0, 'Humidity'] = new_humidity
        soil_df.loc[0, 'pH Level'] = new_ph_level
        soil_df.loc[0, 'rainfall(mm)'] = new_rainfall
        soil_df.loc[0, 'place'] = city
        soil_df.loc[0, 'lat'] = new_lat
        soil_df.loc[0, 'long'] = new_lon


        # Display the updated DataFrame
        st.write(" Soil Data:")
        st.write(soil_df)

        # Add a button to make predictions
        if st.button('Predict Best Crops'):
            top_crops = predict_crop(new_Ni, new_Pho, new_Ki, new_temperature, new_humidity, new_ph_level, new_rainfall)
            with col2:
                st.header("Top 5 Crop Recommendations:")
                # Placeholder for the list of crops
                # st.write("Possible Crops to Grow:")
                for crops in top_crops:
                    for crop in crops:
                        st.write(f"- {crop}")  # Display crops as bullet points

        # Ensure the placeholders are well spaced
        st.write("\n" * 5)


# Ways to improve soil fertility placeholder
# with col3:
#     st.header("Ways to improve the soil fertility + giving locations to nearby fertility stores")
#     # Placeholder for the text and possibly a map or list
#     st.write("Ways to Improve Soil Fertility:")
#     for points in fertility_improvement_points:
#         st.write(f"- {points}")  # Replace with your content



else:
    st.warning("Please create an account or login to access the features.")
