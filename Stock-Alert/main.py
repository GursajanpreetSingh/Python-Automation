import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

response = requests.get(
    STOCK_ENDPOINT, params=stock_params, timeout=15
)
response.raise_for_status()
stock_data = response.json()

if "Time Series (Daily)" not in stock_data:
    raise ValueError(f"Stock API error: {stock_data}")

data_list = list(stock_data["Time Series (Daily)"].values())

yesterday_closing_price = float(data_list[0]["4. close"])
day_before_yesterday_closing_price = float(data_list[1]["4. close"])

difference = yesterday_closing_price - day_before_yesterday_closing_price
diff_percent = (difference / day_before_yesterday_closing_price) * 100

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

print(f"{STOCK} change: {up_down}{diff_percent:.2f}%")

if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 3
    }

    news_response = requests.get(
        NEWS_ENDPOINT, params=news_params, timeout=15
    )
    news_response.raise_for_status()
    news_data = news_response.json()

    if news_data.get("status") != "ok":
        raise ValueError(f"News API error: {news_data}")

    articles = news_data.get("articles", [])[:3]

    if not articles:
        print("No relevant news articles found.")
    else:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        for article in articles:
            headline = article.get("title") or "No title available"
            brief = article.get("description") or "No description available"

            message_body = (
                f"{STOCK}: {up_down}{abs(diff_percent):.2f}%\n"
                f"Headline: {headline}\n"
                f"Brief: {brief}"
            )

            message = client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=MY_PHONE_NUMBER
            )

            print(f"SMS submitted. Status: {message.status}")
else:
    print("Stock movement is within the 5% threshold. No news alert.")