from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from datetime import datetime


class FlightData:
    def __init__(self, city_from_iata_code):
        self.city_from_iata_code = city_from_iata_code

    def compare_flights_and_update(self):
        data_manager = DataManager()
        table_data = data_manager.get_sheet_data()
        flight_search = FlightSearch()
        notification_manager = NotificationManager()

        # Iterate over the Google sheet data and gather the cheapest in date flights.
        
        if table_data:
            for row in table_data:
                # Gather and format the flight data.
                best_value_flight = flight_search.find_cheapest_flight_for(city_code_from=self.city_from_iata_code,
                                                                           city_code_to=row['iataCode'])

                # If the flight search had a successful response compare the data
                if best_value_flight:
                    lowest_current_price = int(best_value_flight['price'])
                    departure = datetime.fromisoformat(best_value_flight['local_departure'][:-1] + '+00:00').strftime(
                        '%d/%m/%Y')

                    # If a new cheaper flight is available or the flight has already departed update the Google sheet.
                    flight_has_departed = datetime.strptime(row['date'], "%d/%m/%Y").date() < datetime.now().date()

                    if int(row['lowestPrice']) > lowest_current_price or flight_has_departed:
                        notification_manager.send_text_alert(best_value_flight)
                        data_manager.update_cell_data(column_name="lowestPrice", row_id=row['id'],
                                                      new_value=lowest_current_price)
                        data_manager.update_cell_data(column_name="date", row_id=row['id'],
                                                      new_value=departure)
