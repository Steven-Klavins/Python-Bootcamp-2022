import os
import requests
from flight_search import FlightSearch

SHEETY_HEADERS = {
    "Authorization": os.getenv("SHEETY_TOKEN")
}

# This class is responsible for talking to the Google Sheet.
class DataManager:
    def get_sheet_data(self):
        response = requests.get(os.getenv("SHEETY_ENDPOINT"), headers=SHEETY_HEADERS)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data['prices']

    # Update a single table cell with a new value
    def update_cell_data(self, column_name, row_id, new_value):

        params = {
            "price": {
                column_name: new_value
            }
        }

        response = requests.put(f"{os.getenv('SHEETY_ENDPOINT')}/{row_id}", headers=SHEETY_HEADERS, json=params)
        response.raise_for_status()

    def update_iata_codes(self):
        sheet_data = self.get_sheet_data()
        flight_search = FlightSearch()

        for row in sheet_data:
            new_iata_code = flight_search.find_city_iata_code(row['city'])
            self.update_cell_data(column_name="iataCode", row_id=(row['id']), new_value=new_iata_code)
