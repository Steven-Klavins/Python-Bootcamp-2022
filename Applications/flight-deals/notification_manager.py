import os
from twilio.rest import Client
from datetime import datetime


class NotificationManager:

    # This class is responsible for sending notifications with the deal flight details.

    # Format the message sent to the user
    def format_flight_message(self, flight_data):
        # Extract the needed values from the flight data
        price = flight_data['price']
        city_from = flight_data['cityFrom']
        fly_from = flight_data['flyFrom']
        city_to = flight_data['cityTo']
        city_code_to = flight_data['cityCodeTo']
        departure = datetime.fromisoformat(flight_data['local_departure'][:-1] + '+00:00').strftime(
            '%d/%m/%Y')

        return f"Low price alert! Only £{price} to fly from {city_from}-{fly_from} to {city_to}-{city_code_to}, on " \
               f"{departure} "

    # Tap into Twilio and send the user a low price alert
    def send_text_alert(self, flight_data):
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        message = client.messages \
            .create(
            body=self.format_flight_message(flight_data),
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=os.getenv("USER_PHONE_NUMBER")
        )
