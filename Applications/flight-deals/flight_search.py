import requests
import os
import datetime
from dateutil.relativedelta import relativedelta
from data_manager import DataManager

KIWI_HEADERS = {
    "apikey": os.getenv("KIWI_API_KEY"),
    "Content-Type": "application/json"
}

class FlightSearch:

    # Return a city's code
    def find_city_iata_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city",
        }
        
        try:
            response = requests.get(url="https://api.tequila.kiwi.com/locations/query", params=params,
                                    headers=KIWI_HEADERS)
            response.raise_for_status()
            data = response.json()
            return data['locations'][0]["code"]
        except requests.exceptions.RequestException as e:
            print(e)
            return False

    def find_cheapest_flight_for(self, city_code_from, city_code_to):
        params = {
            "fly_from": city_code_from,
            "fly_to": city_code_to,
            'adults': '1',
            "date_from": str(datetime.date.today().strftime('%d/%m/%Y')),
            "date_to": str((datetime.date.today() + relativedelta(months=+6)).strftime('%d/%m/%Y')),
            "curr": "GBP",
            "sort": "price"
        }

        try:
            response = requests.get(url="https://api.tequila.kiwi.com/v2/search", headers=KIWI_HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            cheapest_flight = data['data'][0]
            return cheapest_flight
        except requests.exceptions.RequestException as e:
            print(e)
            return False

    # Iterate over the Google sheet city names and ensure all city names have the correct IATA codes
    def update_iata_codes(self):
        data_manager = DataManager()
        sheet_data = data_manager.get_sheet_data()

        # If we successfully gather the sheet data gather IATA codes and make sure they're correct.
        if sheet_data:
            for row in sheet_data:
                new_iata_code = self.find_city_iata_code(row['city'])
                if new_iata_code:
                    data_manager.update_cell_data(column_name="iataCode", row_id=(row['id']), new_value=new_iata_code)
