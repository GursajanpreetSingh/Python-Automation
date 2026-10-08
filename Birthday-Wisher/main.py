import pandas
import smtplib
import datetime as dt
import random
import os
from dotenv import load_dotenv

load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

now = dt.datetime.now()

data = pandas.read_csv("birthdays.csv")
data_dict = data.to_dict(orient="records")

letters = ["letter_1.txt","letter_2.txt","letter_3.txt"]

for line in data_dict:
    if now.month == line['month'] and now.day == line['day']:
        birthday_name = line['name']
        birthday_email = line['email']

        letter = random.choice(letters)

        with open(f"letter_templates/{letter}") as letter_file:
            message = letter_file.read().replace("[NAME]",birthday_name)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,to_addrs=birthday_email,msg=f"Subject:Happy Birthday\n\n{message}")

