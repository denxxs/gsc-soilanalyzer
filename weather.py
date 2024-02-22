import requests
import config

def weather_fetch(lat, lon):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    lat, lon = str(lat), str(lon)
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(complete_url)

    x = response.json()
    # print(x)

    if x["cod"] != "404":
        y = x["main"]
        
        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        # rain = x["rain"] # rain if exists it will show up in x -> api json response
        return temperature, humidity
    else:
        return None
    
# print(weather_fetch(13.0809856, 80.2095104))

# temp, hum = weather_fetch("Boston")
# print("temp:", temp)
# print("humidity:", hum)

# print("rain:", rain)