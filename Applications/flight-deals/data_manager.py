import os
import requests


class DataManager:

    # This class is responsible for talking to the Google Sheet.
    def get_sheet_data(self):
        headers = {
            "Authorization": os.getenv("SHEETY_TOKEN")
        }
        response = requests.get(os.getenv("SHEETY_ENDPOINT"), headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data)
