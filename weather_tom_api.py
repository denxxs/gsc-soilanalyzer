import requests
import csv
import json
from datetime import datetime

url = "https://api.tomorrow.io/v4/weather/history/recent?location=austin&apikey=3IhKa8wYa93k16gxIm3WGDnifTpZXOuE"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
# print(response.text   )

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Handle hourly data
    hourly_data = data["timelines"]["hourly"]
    hourly_file_name = f"weather_hourly_data_{timestamp}.csv"

    with open(hourly_file_name, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['time'] + list(hourly_data[0]['values'].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for entry in hourly_data:
            row = {'time': entry['time'], **entry['values']}
            writer.writerow(row)

    print(f"Hourly data successfully written to {hourly_file_name}")

    # Handle daily data
    daily_data = data["timelines"]["daily"]
    daily_file_name = f"weather_daily_data_{timestamp}.csv"

    with open(daily_file_name, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['time'] + list(daily_data[0]['values'].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for entry in daily_data:
            row = {'time': entry['time'], **entry['values']}
            writer.writerow(row)

    print(f"Daily data successfully written to {daily_file_name}")
else:
    print(f"Failed to get data: {response.status_code}")
