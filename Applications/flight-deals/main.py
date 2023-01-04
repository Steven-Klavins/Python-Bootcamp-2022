from flight_data import FlightData

# Declare your city code here
# This file can be run daily/weekly depending on how frequently you'd like to check flights
fd = FlightData(city_from_iata_code="LON")
fd.compare_flights_and_update()
