import requests
import os


class FlightSearch:
    def __init__(self):
        pass

    # Return a city's code
    def find_city_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city",
        }

        headers = {
            "apikey": os.getenv("KIWI_API_KEY"),
        }

        response = requests.get(url="https://api.tequila.kiwi.com/locations/query", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data['locations'][0]["code"])
