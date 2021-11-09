import urllib.request
from pprint import pprint
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "jvAFXd6tklkqAsG2UtNQAbwzwMHbGC8c"
MBTA_API_KEY = "3c65b5dd370a4f2dbc6c972820af984d"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """ 
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    # pprint(response_data)
    return response_data

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    if " " in place_name:
        place_name = place_name.replace(" ","%20")
    state = "MA"
    city = "Boston"
    locations = (get_json(f"http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name},{state},{city}%20"))
    # pprint(locations)
    pure_location = locations["results"][0]["locations"]
    latitude_longitude = pure_location[0]["latLng"]
    latitude_longitude = (latitude_longitude.values())
    return tuple(latitude_longitude)

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    mbta_data = (get_json(f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"))
    mbta_station = mbta_data["data"][0]["attributes"]['name']
    wheelchair_info = mbta_data["data"][0]["attributes"]["wheelchair_boarding"]
    if wheelchair_info == 0: 
        accessibility = "No W.C Information"
    elif wheelchair_info == 1: 
        accessibility = "W.C Accessible"
    else:
        accessibility = "W.C Inaccessible"
    return (f"{mbta_station}: {accessibility}")

def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    specific_location = get_lat_long(place_name)
    latitude = specific_location[0]
    longitude = specific_location[1]
    return get_nearest_station(latitude,longitude)


def main():
    """
    You can test all the functions here
    """
    # print(get_lat_long("Fenway Park"))
    # print(get_nearest_station(42.34169, -71.09756))
    place_name = input("Please enter a specific location in Boston to view the nearest MBTA station and the wheelchair information: ")
    find_stop_near(place_name)

if __name__ == '__main__':
    main()
