import os
import requests
import re
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
API_NUM = os.getenv("API_NUM")

# Emoji mapping for weather codes
WEATHER_EMOJIS = {
    200: "⛈️", 201: "⛈️", 202: "⛈️", 210: "⛈️", 211: "⛈️", 212: "⛈️", 221: "⛈️",
    230: "⛈️", 231: "⛈️", 232: "⛈️",  # Thunderstorms
    300: "🌧️", 301: "🌧️", 302: "🌧️", 310: "🌧️", 311: "🌧️", 312: "🌧️",
    313: "🌧️", 314: "🌧️", 321: "🌧️",  # Drizzle
    500: "🌧️", 501: "🌧️", 502: "🌧️", 503: "🌧️", 504: "🌧️", 511: "🌧️",
    520: "🌧️", 521: "🌧️", 522: "🌧️", 531: "🌧️",  # Rain
    600: "❄️", 601: "❄️", 602: "❄️", 611: "❄️", 612: "❄️", 613: "❄️",
    615: "❄️", 616: "❄️", 620: "❄️", 621: "❄️", 622: "❄️",  # Snow
    701: "🌫️", 711: "🌫️", 721: "🌫️", 731: "🌫️", 741: "🌫️", 751: "🌫️",
    761: "🌫️", 762: "🌫️", 771: "💨", 781: "🌪️",  # Atmosphere
    800: "☀️",  # Clear sky
    801: "⛅", 802: "⛅", 803: "☁️", 804: "☁️"  # Clouds
}

def get_phone_number() -> str:
    # Prompt for phone number
    user_input = input("Enter your phone number (no spaces or dashes, e.g., 12345678901): ").strip()
    
    # Remove any existing + or non-numeric characters
    cleaned_number = re.sub(r'[^0-9]', '', user_input)
    
    # Assume US number (10 digits + country code +1)
    if len(cleaned_number) == 10:
        user_number = f"+1{cleaned_number}"  # Add +1 for US numbers
    else: #len(cleaned_number) == 11 and cleaned_number.startswith('1'):
        user_number = f"+{cleaned_number}"  # Already includes US country code
    return user_number

def get_coordinates() -> tuple[float, float]:
    default_latitude = 38.435982
    default_longitude = -78.879997

    try:
        # Prompt user for latitude
        latitude = float(input("Enter latitude (-90 to 90): "))
        # Validate latitude
        if not -90 <= latitude <= 90:
            print("Invalid latitude. Using default latitude:", default_latitude)
            latitude = default_latitude
    except ValueError:
        print("Invalid input for latitude. Using default latitude:", default_latitude)
        latitude = default_latitude

    try:
        # Prompt user for longitude
        longitude = float(input("Enter longitude (-180 to 180): "))
        # Validate longitude
        if not -180 <= longitude <= 180:
            print("Invalid longitude. Using default longitude:", default_longitude)
            longitude = default_longitude
    except ValueError:
        print("Invalid input for longitude. Using default longitude:", default_longitude)
        longitude = default_longitude

    return latitude, longitude


def main() -> None:
    latitude, longitude = 38.435982, -78.879997 # get_coordinates()
    user_number = get_phone_number()
    
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "cnt": 4  # requesting time stamps in the near future
    }

    response = requests.get(OWM_ENDPOINT, params=params)
    response.raise_for_status()
    weather_data = response.json()
    
    will_rain = False
    msg = ""
    for i in range(params["cnt"]):
        condition_code = int(weather_data["list"][i]["weather"][0]["id"])
        description = str(weather_data["list"][i]["weather"][0]['description'])
        # print(f"Condition code: {condition_code} | Description: {description}")
        
        # rain or similar conditions
        if condition_code < 600:
            will_rain = True
            msg = f"{description.title()} expected today {WEATHER_EMOJIS[condition_code]}. Make sure to bring an umbrella! ☔️"
            break
    
    if will_rain:
        # print(msg) 
        client = Client(ACCOUNT_SID, AUTH_TOKEN) 
        try: 
            message = client.messages.create(
                body=f"{msg}",
                from_=f"{API_NUM}",
                to=f"{user_number}",
            )
            # print(message.status)
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")
            
        
if __name__ == "__main__":
    main()