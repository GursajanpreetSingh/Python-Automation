import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("PIXELA_USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN")
GRAPH_ID = os.getenv("PIXELA_GRAPH_ID")

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"

HEADERS = {
    "X-USER-TOKEN": TOKEN
}

# Create a pixel for today's study hours
today = datetime.now().strftime("%Y%m%d")
study_hours = input("How many hours did you study today? ").strip()

try:
    hours = float(study_hours)
    if hours < 0:
        raise ValueError("Study hours cannot be negative.")

    pixel_data = {
        "date": today,
        "quantity": str(hours)
    }

    response = requests.post(
        url=GRAPH_ENDPOINT,
        json=pixel_data,
        headers=HEADERS,
        timeout=10
    )
    response.raise_for_status()
    print("Pixel creation response:", response.text)

except ValueError as error:
    print(f"Invalid study hours: {error}")
except requests.RequestException as error:
    print(f"Request failed: {error}")

# Update a pixel for a specific date when needed
update_date = datetime(year=2025, month=4, day=22).strftime("%Y%m%d")
update_endpoint = f"{GRAPH_ENDPOINT}/{update_date}"

new_pixel_data = {
    "quantity": "3.5"
}

# Uncomment to update the pixel:
# response = requests.put(
#     url=update_endpoint,
#     json=new_pixel_data,
#     headers=HEADERS,
#     timeout=10
# )
# print(response.status_code, response.text)

# Delete a pixel for a specific date when needed
delete_date = datetime(year=2025, month=4, day=22).strftime("%Y%m%d")
delete_endpoint = f"{GRAPH_ENDPOINT}/{delete_date}"

# Uncomment to delete the pixel:
# response = requests.delete(
#     url=delete_endpoint,
#     headers=HEADERS,
#     timeout=10
# )
# print(response.status_code, response.text)