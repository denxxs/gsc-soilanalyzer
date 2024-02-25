import streamlit as st
import pandas as pd
import numpy as np
import pickle
from streamlit_geolocation import streamlit_geolocation
import os
from datetime import datetime # for testing ig -- get current time
import psycopg2
from dotenv import load_dotenv
from functions import average_image_color, get_city_name, get_weather
from chattester import chatbot


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

# initialize session state for recommendation and chatbot page status
if 'show_recommendation' not in st.session_state:
    st.session_state['show_recommendation'] = False
if 'show_chatbot' not in st.session_state:
    st.session_state['show_chatbot'] = False



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

def recommendation_page():
    def soil_datatable(soil_df, new_Ni, new_Pho, new_Ki, new_temperature, new_humidity, new_ph_level, new_rainfall, city, new_lat, new_lon):

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
        st.write(" Soil Data:(NPK values are ratio)")
        st.write(soil_df)

        # Add a button to make predictions
        if st.button('Predict Best Crops'):
            top_crops = predict_crop(new_Ni, new_Pho, new_Ki, new_temperature, new_humidity, new_ph_level, new_rainfall)
            with col2:
                st.header("Top 5 Crop Recommendations:")
                # Placeholder for the list of crops
                # st.write("Possible Crops to Grow:")
                for crops in top_crops:
                    st.write(f"- {crops}")  # Display crops as bullet points

        return 
        # Ensure the placeholders are well spaced
        st.write("\n" * 5)

    # Menu bar for user selection
    menu_options = ["Get User from Sensor", "Use Camera", "Upload Manually"]
    selected_option = st.selectbox("Choose an option:", menu_options)

    if selected_option == "Get User from Sensor":
        # Code to handle sensor input
        st.header("Sensor input functionality")

        # Download sensor file link
        link = "https://www.youtube.com/"
        st.markdown(f'<a href="{link}" target="_blank">Click here to download sensor files</a>', unsafe_allow_html=True)


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
            'N': nrat,
            'P': prat,
            'K': krat,
            'Temperature (°C)': [0.0],
            'Humidity': [0.0],
            'pH Level': [7.0],  # Default value, adjust as needed
            'rainfall(mm)': [150.9],  # Default value, adjust as needed
            'place' : ['Chennai'],
            'lat': [0.0],
            'long': [0.0]
        }
        
        soil_df = pd.DataFrame(soil_data)
        
        # Columns for the soil type image and the two sections on the right
        col1, col2 = st.columns([4, 2])

        # Soil type image placeholder
        with col1:
            # pH Level
            new_ph_level = st.number_input("pH Level", value=soil_df.loc[0, 'pH Level'])

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
            tem = (tem + new_temperature) / 2
            mois = (mois + new_humidity) / 2

            soil_datatable(soil_df, nrat, prat, krat, tem, mois, new_ph_level, new_rainfall, city, new_lat, new_lon)


    elif selected_option == "Use Camera":
        # Code to handle camera input
        st.write("Camera functionality")
        
        # Upload file button for JPEG files
        uploaded_file = st.file_uploader("Upload a JPEG file", type=["jpeg", "jpg"])
        if uploaded_file is not None:
            # Code to handle the uploaded JPEG file
            st.write("File uploaded successfully.")
            k, p, n = average_image_color(uploaded_file)
            
            
            # Define initial soil data with values retrieved from the database
            soil_data = {
                'N': n,
                'P': p,
                'K': k,
                'Temperature (°C)': [0.0],
                'Humidity': [0.0],
                'pH Level': [7.0],  # Default value, adjust as needed
                'rainfall(mm)': [150.9],  # Default value, adjust as needed
                'place' : ['Chennai'],
                'lat': [0.0],
                'long': [0.0]
            }
            
            soil_df = pd.DataFrame(soil_data)
            
            # Columns for the soil type image and the two sections on the right
            col1, col2 = st.columns([4, 2])

            # Soil type image placeholder
            with col1:
                # pH Level
                new_ph_level = st.number_input("pH Level", value=soil_df.loc[0, 'pH Level'])

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
                
                soil_datatable(soil_df, n, p, k, new_temperature, new_humidity, new_ph_level, new_rainfall, city, new_lat, new_lon)


    elif selected_option == "Upload Manually":
        st.header('Input values Manually')
        # Define initial soil data with values retrieved from the database
        soil_data = {
            'N': [0.0],
            'P': [0.0],
            'K': [0.0],
            'Temperature (°C)': [0.0],
            'Humidity': [0.0],
            'pH Level': [7.0],  # Default value, adjust as needed
            'rainfall(mm)': [150.9],  # Default value, adjust as needed
            'place' : ['Chennai'],
            'lat': [0.0],
            'long': [0.0]
        }
        
        soil_df = pd.DataFrame(soil_data)
        
        # Columns for the soil type image and the two sections on the right
        col1, col2 = st.columns([4, 2])

        # Soil type image placeholder
        with col1:
            # Editable Soil Data
            # Display editable DataFrame using st.columns()
            st.header("Editable Soil Data")

            # Columns for the soil data
            # location, Ni, Pho, Ki, temperature, humidity, ph_level, rainfall = st.columns(8)
            cord, Ni, Pho, Ki, ph_level = st.columns(5)

            # N level
            with Ni:
                new_Ni = st.number_input("N", value=soil_df.loc[0, 'N'])

            # P level
            with Pho:
                new_Pho = st.number_input("P", value=soil_df.loc[0, 'P'])

            # K level
            with Ki:
                new_Ki = st.number_input("K", value=soil_df.loc[0, 'K'])
                
            # pH Level
            with ph_level:
                new_ph_level = st.number_input("pH Level", value=soil_df.loc[0, 'pH Level'])

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

            total_sum = new_Ni + new_Pho + new_Ki
            # Check if the total_sum is not zero to avoid division by zero
            if total_sum != 0:
                r = (new_Ni / total_sum) * 6
                g = (new_Pho / total_sum) * 6
                b = (new_Ki / total_sum) * 6
            else:
                # Handle the case where total_sum is zero
                r, g, b = 0, 0, 0  # or any other default valu1
                
            soil_datatable(soil_df, r, g, b, new_temperature, new_humidity, new_ph_level, new_rainfall, city, new_lat, new_lon)

        # with col2:
        #     st.header("Soil Type")
        #     st.image("static/soil.png", use_column_width=True, output_format='auto')  # Replace with your image path


    # Ways to improve soil fertility placeholder
    # with col3:
    #     st.header("Ways to improve the soil fertility + giving locations to nearby fertility stores")
    #     # Placeholder for the text and possibly a map or list
    #     st.write("Ways to Improve Soil Fertility:")
    #     for points in fertility_improvement_points:
    #         st.write(f"- {points}")  # Replace with your content

def chatbot_page():
    st.header('chatbot')

# Sidebar for Account Creation and Login
with st.sidebar:
    st.header("Authentication")
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
    with st.sidebar:
        st.subheader("Navigation")
        # Create a widebar sidebar button
        if st.button('Crop Recommendation'):
            st.session_state['show_recommendation'] = True
            st.session_state['show_chatbot'] = False
        if st.button('ChatBot - Google Gemini Model'):
            st.session_state['show_chatbot'] = True
            st.session_state['show_recommendation'] = False

    
    if st.session_state['show_recommendation']:
        recommendation_page()
    if st.session_state['show_chatbot']:
        chatbot()

else:
    st.warning("Please create an account or login to access the features.")
