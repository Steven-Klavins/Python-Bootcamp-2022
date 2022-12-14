import os
import requests

SHEETY_HEADERS = {
    "Authorization": os.getenv("SHEETY_TOKEN")
}


# This class is responsible for talking to the Google Sheet.
class DataManager:
    # Collect all the Google sheet data
    def get_sheet_data(self):
        try:
            response = requests.get(os.getenv("SHEETY_ENDPOINT"), headers=SHEETY_HEADERS)
            response.raise_for_status()
            data = response.json()
            return data['prices']
        except requests.exceptions.RequestException as e:
            print(e)
            return False

    # Update a single table cell with a new value
    def update_cell_data(self, column_name, row_id, new_value):
        params = {
            "price": {
                column_name: new_value
            }
        }
        try:
            response = requests.put(f"{os.getenv('SHEETY_ENDPOINT')}/{row_id}", headers=SHEETY_HEADERS, json=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)


