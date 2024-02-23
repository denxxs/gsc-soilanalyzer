import requests
import config

def get_weather(city, time):
    """
    Fetch and returns the temperature and humidity of a city
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



# time_string = "2024-02-23 12:50:32.23" # time format example

# print(get_weather("chennai", time_string))
