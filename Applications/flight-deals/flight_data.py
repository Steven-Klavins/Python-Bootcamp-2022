from flight_search import FlightSearch
from data_manager import DataManager


class FlightData:
    def __init__(self, city_from_iata_code):
        self.city_from_iata_code = city_from_iata_code

    def compare_flights_and_update(self):
        data_manager = DataManager()
        table_data = data_manager.get_sheet_data()
        flight_search = FlightSearch()

        for row in table_data:
            lowest_current_value = int(flight_search.find_cheapest_flight_for(city_code_from=self.city_from_iata_code,
                                                                              city_code_to=row['iataCode'])['price'])
            print(lowest_current_value)
            print(row['lowestPrice'])
            if int(row['lowestPrice']) > lowest_current_value:
                data_manager.update_cell_data(column_name="lowestPrice", row_id=row['id'],
                                              new_value=lowest_current_value)
