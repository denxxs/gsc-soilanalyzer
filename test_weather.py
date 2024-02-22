import requests
import config  # Assuming you have a config.py file with your API key defined as weather_api_key

def get_weather(lat, lon, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    return data

# Example usage:
lat, lon = 40.7128, -74.0060  # Example latitude and longitude (New York City)
api_key = config.weather_api_key

weather_data = get_weather(lat, lon, api_key)

if 'rain' in weather_data:
    print("Rainfall:", weather_data['rain'])
else:
    print("No rainfall data available.")
