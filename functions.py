from PIL import Image
import numpy as np
from geopy.geocoders import Nominatim
import requests
import config
import streamlit as st
import pickle

def average_image_color(filename):
    '''
    param - filename/uploaded file
    return - n, p, k ratio 
    '''
    img = Image.open(filename).convert('RGB')
    pixels = np.array(img)

    # Calculate the average RGB values
    average_color = pixels.mean(axis=(0, 1))
    rgb=list(average_color)

    r = (rgb[0])
    g = (rgb[1])
    b = (rgb[2]) 

    sum = r + g + b
     # Check if the total_sum is not zero to avoid division by zero
    if sum != 0:
        k = (r / sum) * 6
        p = (g / sum) * 6
        n = (b / sum) * 6
    else:
        # Handle the case where total_sum is zero
        k, p, n = 0, 0, 0  # or any other default valu1

    return k, p, n


def get_city_name(lat, long):
    '''
    takes 
    param - latitude, longitude
    returns - city name
    '''
    try:
        geolocator = Nominatim(user_agent="reverse_geocode")
        location = geolocator.reverse((lat, long))

        if location is not None:
            location_dict = location.raw['address']
            # print(location_dict)
            # Check for keys in order of preference
            if 'city' in location_dict:
                return location_dict['city']
            elif 'town' in location_dict:
                return location_dict['town']
            elif 'village' in location_dict:
                return location_dict['village']
            elif 'suburb' in location_dict:
                return location_dict['suburb']
            else:
                return "Location not found"
        else:
            return "No location data"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error in geolocation service"
# # Example usage
# latitude = 12.9401
# longitude = 80.1866
# city_name = get_city_name(latitude, longitude)
# print(city_name)

def get_weather(city, time):
    """
    Fetch and returns the avg temperature, avg humidity, avg rainfall of a city for the next 30 days
    :params: city, time
    :return: avg_temp, avg_humidity, avg_precip
    """
    # visual crossing API key
    api_key = config.visualcrossing_api_key

    # split time parameter -- take from database
    date_string, time_part = time.split(' ')

    # Further splitting the date
    year, month, day = date_string.split('-')
    
    future_month = int(month) + 1
    if future_month > 12:
        future_month = future_month - 12
    future_month = str(future_month)

    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}%2C%20TN%2C%20IN/{date_string}/{year}-{future_month}-{day}?unitGroup=metric&key={api_key}&include=fcst"
    
    # complete_url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    # Initialize sums
    total_temp = 0.0
    total_humidity = 0.0
    total_precip = 0.0
    count = 0

    # Process each day
    for day_data in data['days']:
        if 'temp' in day_data and day_data['temp'] is not None:
            total_temp += day_data['temp']
            count += 1
        if 'humidity' in day_data and day_data['humidity'] is not None:
            total_humidity += day_data['humidity']
        if 'precip' in day_data and day_data['precip'] is not None:
            total_precip += day_data['precip']

    # Calculating averages
    avg_temp = total_temp / count if count > 0 else 0
    avg_humidity = total_humidity / count if count > 0 else 0
    avg_precip = total_precip / count if count > 0 else 0

    return avg_temp, avg_humidity, avg_precip



# time_string = "2024-02-23 07:16:11.159179" # time format example

# print(get_weather("chennai", time_string))

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
