# Public API ID and API KEY for getting the direction datas
APP_ID = "62697aef"
API_KEY = "1f848e5a96335450ce5f1b9969f7ee38"

# Importing required libraries
import urllib.request
import json
import pyttsx3
import requests
from geopy.geocoders import Nominatim


def data_gathering():
    """This is the most important function which is used to get the live location of the person through
    the api and calculates the directions by the given destination with km and time"""
    # Getting live lattitude and longitude data from the ip-api
    response = requests.get("http://ip-api.com/json/103.220.210.215").json()

    # Latitude and longitude extraction
    latitude = response['lat']+1
    longitude = response['lon']

    # Your Bing Maps Api Key
    bingMapsKey = "ApFr1grOeMUw9DEV4sPm60bcgz1Ye6flK6FHfPqN97tDp0BsJVsf9uQxA1Myo2AF"

    # Selecting the destination
    destination = "lulu mall bengaluru"

    # Getting the json from microsoft bing maps api
    encodedDest = urllib.parse.quote(destination, safe='')
    # Accessing json data
    routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(
        longitude) + "&wp.1=" + encodedDest + "&key=" + bingMapsKey
    # Opening the url using request and storing the returned response
    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)

    # Reading the json file
    r = response.read().decode(encoding="utf-8")
    result = json.loads(r)

    # Accessing the lattitude and longitude and directions
    itineraryItems = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]

    # Seperating the json dictionary data into seperate keys
    direction = []
    for item in itineraryItems:
        direction_data = item["instruction"]["text"]
        lattitude = item["maneuverPoint"]["coordinates"][0]
        longitude = item["maneuverPoint"]["coordinates"][1]
        direction.append(direction_data)
        # Returning the direction list with lattitude and longitude embededed with it
    return direction, lattitude, longitude


def get_current_location():
    """This function is used to get the lattitude and longitude from the data_gathering function and stores it into
    google sheet which was converted into a api using Sheety api. The main usage of this is to create a telegram bot
    to show the live location of the person with one tap also this is embedded with voice command in the GUI Part"""

    lattitude = data_gathering()[1]
    longitude = data_gathering()[2]
    sheet_endpoint = "https://api.sheety.co/53a30481e81efdd742e5ec33978c079d/gpsData/sheet1"
    # Giving authentication access
    header = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY
    }

    # Importing the lattitude and longitude data to sheet1
    sheet_inputs = {
        "sheet1": {
            "lattitude": lattitude,
            "longitude": longitude,

        }
    }
    requests.post(sheet_endpoint, json=sheet_inputs)


def current_location_address():
    """Getting the current address from the lattitude and longitude and which is embedded in voice command for Visually Impared
    Members"""
    # Speech Engine
    engine = pyttsx3.init()
    # Accessing GetLoc Api
    geoLoc = Nominatim(user_agent="GetLoc")
    # Getting address from the lat and long
    locname = geoLoc.reverse(f"{data_gathering()[1]}, {data_gathering()[2]}")
    print(locname.address)
    engine.say("Now you are at," + locname.address)
    engine.runAndWait()
    return locname.address


def location_change_checks():
    """This is a complex programming which is the shorter way to calculate the next check point from the
    live lattitude,longitude and the distance to the next checkpoint"""
    changed = True
    data_direction = data_gathering()[0]
    flag = True

    while flag:
        try:
            data_direction2 = data_gathering()[0]
            # Checking for the previous and next check points
            if data_direction2[0] == data_direction[2]:
                return None
            else:
                data_direction = data_direction2.copy()
                flag = False
                return data_direction[0]

        except:
            print("Error Found at Data Gathering")
            break

if __name__ == "__main__":
    # Map Navigation Data
    engine = pyttsx3.init()
    while True:
        # It will reply to  the next checkpoint when they are on the way towards the checkpoints
        if location_change_checks() != None:
            data1 = location_change_checks()
            print(data1)
            engine.say("OK good")
            engine.say("Now," + data1)
            engine.runAndWait()
            break
