import streamlit as st
import pandas as pd
import numpy as np

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# Define initial soil data
soil_data = {
    'location': ['Chennai'],
    'pH Level': [6.5],
    'Humidity (%)': [30],
    'Temperature (°C)': [22],
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
col1, col2, col3 = st.columns([2, 1, 1])

# Soil type image placeholder
with col1:
    st.header("Related Soil Type Image Here")
    # Placeholder for the image
    st.image("soil.png", use_column_width=True, output_format='auto')  # Replace with your image path

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
with col2:
    st.header("List of crops you can grow in this soil")
    # Placeholder for the list of crops
    st.write("Possible Crops to Grow:")
    for crop in possible_crops:
        st.write(f"- {crop}")  # Display crops as bullet points


# Ways to improve soil fertility placeholder
with col3:
    st.header("Ways to improve the soil fertility + giving locations to nearby fertility stores")
    # Placeholder for the text and possibly a map or list
    st.write("Ways to Improve Soil Fertility:")
    for points in fertility_improvement_points:
        st.write(f"- {points}")  # Replace with your content


# Editable Soil Data
# Display editable DataFrame using st.columns()
st.header("Editable Soil Data")

# Columns for the soil data
location, ph_level, humidity, temperature = st.columns(4)

# pH Level
with ph_level:
    new_ph_level = st.number_input("pH Level", value=soil_df.loc[0, 'pH Level'])

# Humidity
with humidity:
    new_humidity = st.number_input("Humidity (%)", value=soil_df.loc[0, 'Humidity (%)'])

# Temperature
with temperature:
    new_temperature = st.number_input("Temperature (°C)", value=soil_df.loc[0, 'Temperature (°C)'])

with location:
    new_location = st.text_input("Location Name", value=soil_df.loc[0, 'location'])

# Update the DataFrame with new values
soil_df.loc[0, 'pH Level'] = new_ph_level
soil_df.loc[0, 'Humidity (%)'] = new_humidity
soil_df.loc[0, 'Temperature (°C)'] = new_temperature
soil_df.loc[0, 'location'] = new_location

# Display the updated DataFrame
st.write(" Soil Data:")
st.write(soil_df)


# Ensure the placeholders are well spaced
st.write("\n" * 5)
