from geopy.geocoders import Nominatim

def get_city_name(lat, long):
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
