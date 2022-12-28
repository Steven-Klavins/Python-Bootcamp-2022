import os
import requests
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

flight_search = FlightSearch()
flight_search.find_city_code(city_name="London")