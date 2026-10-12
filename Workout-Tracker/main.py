import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

auth_header = {
    "Authorization": f"Bearer {os.environ['ENV_SHEETY_TOKEN']}"
}

USERNAME = os.environ["ENV_SHEETY_USERNAME"]
PASSWORD= os.environ["ENV_SHEETY_PASSWORD"]

header = {
    "x-app-id": APP_ID,
    "x-app-key":API_KEY
}

params = {
    "query": input("tell me which exercises you did:")
}

response = requests.post(url=API_ENDPOINT, json=params,headers=header)
data = response.json()
print(data)

for item in data['exercises']:
    Exercise = item["user_input"].title()
    Duration = item["duration_min"]
    Calories = item["nf_calories"]

    today_date = datetime.now().date()
    today_date = today_date.strftime("%d/%m/%Y")
    today_time = datetime.now().time()
    today_time = today_time.strftime("%H:%M:%S")

    params = {
        "workout":{
        "date":today_date,
        "time":today_time,
        "exercise":Exercise,
        "duration":Duration,
        "calories":Calories
        }
    }
    SHEETY_ENDPOINT = os.environ["ENV_SHEETY_ENDPOINT"]

    post_response = requests.post(url=SHEETY_ENDPOINT,json=params,headers=auth_header)
    print(post_response.text)

    # post_response = requests.post(url=SHEETY_ENDPOINT, json=params, auth=(USERNAME,PASSWORD))
    # print(post_response.text)

