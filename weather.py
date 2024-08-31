from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import pytz
from datetime import datetime


load_dotenv()

def get_current_weather(city="Kansas City"):
    request_url= f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=metric'

    weather_data = requests.get(request_url).json()

    # Get timezone offset and create a timezone object
    timezone_offset = weather_data['timezone'] / 60
    local_timezone = pytz.FixedOffset(timezone_offset)
    
    # Get local time in the timezone
    local_time = datetime.now(local_timezone).strftime('%H:%M:%S')
    hour = datetime.now(local_timezone).hour

    # Determine day or night
    day_or_night = "day" if 6 <= hour < 18 else "night"


    # Add local_time to the data
    weather_data['local_time'] = local_time

    # Determine weather category
    weather_description = weather_data["weather"][0]["main"].lower()
    if weather_description == "clear":
        weather_category = "clear"
    elif weather_description in ["clouds", "mist", "fog", "haze", "dust"]:
        weather_category = "clouds"
    elif weather_description in ["rain", "drizzle", "thunderstorm"]:
        weather_category = "rain"
    elif weather_description == "snow":
        weather_category = "snow"
    else:
        weather_category = "clear"

    # Create background image filename
    bg_image = f"{weather_category}_{day_or_night}.jpg"

    return weather_data, bg_image

if __name__ == "__main__":
    print('\n***Get Weather Conditions***')
    city = input("\nPlease enter a city name: ")
    if not bool(city.strip()):
        city = "New Delhi"
    weather_data = get_current_weather(city)
    print("\n")
    pprint(weather_data)

