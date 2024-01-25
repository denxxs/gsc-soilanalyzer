import streamlit as st
import pandas as pd

soil_data = {
    'Fertility': ['Good'],
    'pH Level': [6.5],  # Neutral soil pH
    'Humidity (%)': [30],  # Percentage of soil moisture
    'Temperature (°C)': [22]  # Soil temperature in Celsius
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
fertility_improvement_points = [
    "Regular soil testing",
    "Proper fertilization",
    "Crop rotation",
    "Organic matter addition",
    "Controlled irrigation"
]
# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# Top-level header with a logout button
st.sidebar.header("Logout")

# Columns for the soil type image and the two sections on the right
col1, col2, col3 = st.columns([2, 1, 1])

# Soil type image placeholder
with col1:
    st.header("Related Soil Type Image Here")
    # Placeholder for the image
    st.image("soil.png")  # Replace with your image path

# Tabular information placeholder
with col2:
    st.header("Tabular information and results about the input soil type")
    # Placeholder for the tabular data
    st.write("Soil Sample Data:")
    st.dataframe(soil_df)  # Replace with your DataFrame or table

# List of crops placeholder
with col2:
    st.header("List of crops you can grow in this soil")
    # Placeholder for the list of crops
    st.write("Possible Crops to Grow:")
    st.write(possible_crops)  # Replace with your list

# Ways to improve soil fertility placeholder
with col3:
    st.header("Ways to improve the soil fertility + giving locations to nearby fertility stores")
    # Placeholder for the text and possibly a map or list
    st.write("Ways to Improve Soil Fertility:")
    st.write(fertility_improvement_points)  # Replace with your content

# Ensure the placeholders are well spaced
st.write("\n" * 5)
