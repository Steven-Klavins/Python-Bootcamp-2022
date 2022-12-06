import requests
from datetime import datetime
import smtplib
import time
import os

# Constants

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude

EMAIL = "sample-email@email.com"
PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_PROVIDER = "smtp.gmail.com"

# Attempt to get ISS information

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Attempt to get the current hours the sun rises and sets in your location

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()


# Send an email if the ISS is in view of your location

def is_in_view():
    if (iss_latitude - 5) <= MY_LAT <= (iss_latitude + 5) and (iss_longitude - 5) <= MY_LONG <= (iss_longitude + 5):
        with smtplib.SMTP(SMTP_PROVIDER) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject: Look up!\n\nLook above you, the ISS is overhead!")


# Every 60 seconds check to see if its before sunrise and after sunset before running is_in_view

while True:
    time.sleep(60)
    if time_now.hour > sunset or time_now.hour < sunrise:
        is_in_view()


