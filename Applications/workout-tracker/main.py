import os
import requests
import datetime as dt

# Environment variables

NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_BEARER_TOKEN = os.getenv("SHEETY_BEARER_TOKEN")

# Get user to enter some information about there workout e.g. "Ran for 3 miles"
sentence = input("Tell us what exercises you did \n")

# Pass this information to the Nutritionix APi

nutritionix_params = {
    "query": sentence,
}

nutritionix_headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}

response = requests.post("https://trackapi.nutritionix.com/v2/natural/exercise", headers=nutritionix_headers,
                         json=nutritionix_params)
response.raise_for_status()
data = response.json()['exercises'][0]

# Gather the relevant data from the response

date = dt.date.today().strftime("%d/%m/%Y")
time = dt.datetime.now().strftime("%H:%M:%S")
exercise = data['name'].title()
duration = data['duration_min']
calories = data['nf_calories']

# Submit the data to the Google spreadsheet using the Sheety API

# Cells with dates/times are often inputted with a single ` quote mark appended
# This happens as dates/time in google sheets are stored as serial number format, not a strings.
# Setting valueInputOption=user_entered treats the date/time entered as if you typed it into the Google Sheets UI,
# this automatically converts the string value for us.

workout_params = {
    "valueInputOption": "user_entered"
}

workout_auth_headers = {
 "Authorization": SHEETY_BEARER_TOKEN
}

workout_data = {
    "workout": {
        "date": date,
        "time": time,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

response = requests.post(SHEETY_ENDPOINT, json=workout_data, params=workout_params, headers=workout_auth_headers)
response.raise_for_status()

