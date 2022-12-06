import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Twilio
twilio_account_sid = os.environ.get("ACCOUNT_SID")
twilio_auth_token = os.environ.get("AUTH_TOKEN")

# Open weather map
own_api_key = os.environ.get("OWM_API_KEY")

# Twilio phone number
phone_num_to = os.environ.get("PHONE_NUM_TO")
# Personal phone number
phone_num_from = os.environ.get("PHONE_NUM_FROM")

# Your coordinates
MY_LAT = 51.507351
MY_LONG = -0.127758

END_POINT = "https://api.openweathermap.org/data/3.0/onecall"

# Parameters for API
api_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": own_api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(END_POINT, params=api_params)
response.raise_for_status()
data = response.json()

will_rain = False

for index in range(1, 12):
    if int(data["hourly"][index]['weather'][0]["id"]) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(twilio_account_sid, twilio_auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Bring an umbrella!",
        from_=phone_num_from,
        to=phone_num_to
    )

    print(message.status)
