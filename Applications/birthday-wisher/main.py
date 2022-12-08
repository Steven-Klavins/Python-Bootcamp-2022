import pandas
import random
import smtplib
import datetime as dt
import os

# SMPT constants

EMAIL = "youremail@smtpprovider.com"
PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_PROVIDER = "smtp.gmail.com"


def send_email(email, message):
    # Add email subject to message
    message_with_subject = f"Subject:Happy Birthday \n\n" + ''.join(message)

    # Send the email
    with smtplib.SMTP(SMTP_PROVIDER) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=email, msg=message_with_subject)


def create_birthday_message(birthday):
    # Create one of the 3 template file paths
    template_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"

    # If the template is missing fall back on a default message of Happy Birthday "name"!

    try:
        with open(template_path, 'r', encoding="utf-8") as file:
            birthday_message = file.readlines()
            birthday_message[0] = birthday_message[0].replace("[NAME]", birthday['name'])
    except FileNotFoundError:
        return f"Subject:Happy Birthday \n\n Happy Birthday {birthday['name']}!"

    return birthday_message


def check_for_birthdays(birthday_list):
    today = dt.datetime.now()
    day_month = today.strftime("%d/%m")

    # Check to see if anyone in the birthday list matches the present month and day

    for birthday in birthday_list:
        if f"{birthday['day']}/{birthday['month']}" == day_month:
            message = create_birthday_message(birthday)
            send_email(birthday['email'], message)


# Attempt to open the birthdays list, if it does not exist create a placeholder
# If it does check the list using the check_for_birthdays method

try:
    with open("birthdays.csv", 'r', encoding="utf-8") as file:
        birthdays = pandas.read_csv("birthdays.csv").to_dict(orient="records")
        check_for_birthdays(birthdays)
except FileNotFoundError:
    with open("./data/words_to_learn.csv", 'w', encoding="utf-8") as file:
        file.write("name,email,year,month,day\n")
