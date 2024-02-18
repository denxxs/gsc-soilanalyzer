import streamlit as st
import pandas as pd
import numpy as np
import pickle
from weather import weather_fetch
import os


# Set the page configuration to wide layout
st.set_page_config(layout="wide")


# Making crop recommendation
def predict_crop(new_Ni, new_Pho, new_Ki, new_temperature, new_humidity, new_ph_level, new_rainfall):

    # Load the model from the .pkl file
    with open('models/RandomForest.pkl', 'rb') as file:
        model = pickle.load(file)

    soil_dataValue = np.array([[new_Ni, new_Pho, new_Ki, new_temperature, new_humidity, new_ph_level, new_rainfall]])
    # Get probabilities for each class
    probabilities = model.predict_proba(soil_dataValue)

    # Get the indices of the classes sorted by probability in descending order
    top_5_indices = np.argsort(probabilities, axis=1)[:, ::-1][:, :5]

    # Get the corresponding class names for the top 5 indices
    top_5_crops = model.classes_[top_5_indices]

    # return the top 5 crop predictions
    return top_5_crops


# Define initial soil data
soil_data = {
    'N': [83],
    'P': [45],
    'K': [60],
    'Temperature (°C)': [28.0],
    'Humidity': [70.3],
    'pH Level': [7.0],
    'rainfall(mm)': [150.9],
    'location': ['Chennai']
}
soil_df = pd.DataFrame(soil_data)

possible_crops = [
    "Wheat",
    "Corn",
    "Rice",
    "Barley",
    "Soybeans",
    "Tomatoes"
]
possible_crops_df = pd.DataFrame(possible_crops)
fertility_improvement_points = [
    "Regular soil testing",
    "Proper fertilization",
    "Crop rotation",
    "Organic matter addition",
    "Controlled irrigation"
]


# Top-level header with a logout button
st.sidebar.header("Logout")

# Columns for the soil type image and the two sections on the right
col1, col2 = st.columns([2, 4])

# Soil type image placeholder
with col1:
    st.header("Related Soil Type Image Here")
    # Placeholder for the image
    st.image("static/soil.png", use_column_width=True, output_format='auto')  # Replace with your image path

# with col1:
#     st.header("Tabular information and results about the input soil type")
#     # Placeholder for the tabular data
#     st.write("Soil Fertility Data:")
#     st.dataframe(soil_df)  # Replace with your DataFrame or table

# # Tabular information placeholder
# with col2:
#     st.header("Tabular information and results about the input soil type")
#     # Placeholder for the tabular data
#     st.write("Soil Sample Data:")
#     st.dataframe(soil_df)  # Replace with your DataFrame or table

# List of crops placeholder
# with col2:
#     st.header("List of crops you can grow in this soil")
#     # Placeholder for the list of crops
#     st.write("Possible Crops to Grow:")
#     print('possible', possible_crops)
#     for crop in possible_crops:
#         st.write(f"- {crop}")  # Display crops as bullet points


# Ways to improve soil fertility placeholder
# with col3:
#     st.header("Ways to improve the soil fertility + giving locations to nearby fertility stores")
#     # Placeholder for the text and possibly a map or list
#     st.write("Ways to Improve Soil Fertility:")
#     for points in fertility_improvement_points:
#         st.write(f"- {points}")  # Replace with your content

with col2:
    # Editable Soil Data
    # Display editable DataFrame using st.columns()
    st.header("Editable Soil Data")

    # Columns for the soil data
    # location, Ni, Pho, Ki, temperature, humidity, ph_level, rainfall = st.columns(8)
    location, Ni, Pho, Ki, ph_level, rainfall = st.columns(6)

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
    with location:
        new_location = st.text_input("Location Name", value=soil_df.loc[0, 'location'])
        # update temp and humidity with weather_fetch
        new_temperature, new_humidity = weather_fetch(new_location)

    # Update the DataFrame with new values
    soil_df.loc[0, 'N'] = new_Ni
    soil_df.loc[0, 'P'] = new_Pho
    soil_df.loc[0, 'K'] = new_Ki
    soil_df.loc[0, 'Temperature (°C)'] = new_temperature
    soil_df.loc[0, 'Humidity'] = new_humidity
    soil_df.loc[0, 'pH Level'] = new_ph_level
    soil_df.loc[0, 'rainfall(mm)'] = new_rainfall
    soil_df.loc[0, 'location'] = new_location

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
