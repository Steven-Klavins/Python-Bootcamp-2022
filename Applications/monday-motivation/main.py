import random
import smtplib
import datetime as dt
import os

EMAIL = "sample-email@email.com"
PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_PROVIDER = "smtp.gmail.com"


def send_email():
    with open('quotes.txt', 'r') as file:
        quote = random.choice(file.readlines())

    message = f"Subject:Monday Motivation \n\n {quote}"
    with smtplib.SMTP(SMTP_PROVIDER) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=message)

# On Modays send a quote
if dt.datetime.now().weekday() == 0:
    send_email()
