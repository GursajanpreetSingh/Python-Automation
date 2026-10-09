import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

OWN_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

API_KEY = os.getenv("OPENWEATHER_API_KEY")
MY_LAT = 29.986958
MY_LONG = 75.078621

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(
    url=OWN_ENDPOINT,
    params=weather_params,
    timeout=10
)
response.raise_for_status()
weather_data = response.json()

will_rain = any(
    hour_data["weather"][0]["id"] < 700
    for hour_data in weather_data["list"]
)

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_=TWILIO_PHONE_NUMBER,
        to=MY_PHONE_NUMBER
    )

    print(f"Rain alert sent. Status: {message.status}")
else:
    print("No rain expected in the forecast checked.")