import os
import requests
from bs4 import BeautifulSoup
import smtplib

PRODUCT_URL = "https://www.amazon.co.uk/Gigabyte-GeForce-3070-VISION-Graphics/dp/B095X7XXQK/ref=sr_1_1?keywords=rtx+3080+vision&qid=1673852909&sprefix=rtx+3080+vi%2Caps%2C76&sr=8-1"
YOUR_MAX_PRICE = 900
SMTP_PROVIDER = "smtp.gmail.com"
EMAIL = "youremail@gmail.com"
CURRENCY = "£"

# Add headers to pass the Amazon browser checks.
headers = {
    "User-Agent": "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9"
}


def send_email(product, price):
    # Add email subject to message.
    message = f"{product} is now only {CURRENCY}{price}!"
    # Ensure message is encoded in utf8 to allow £,$,€
    message.encode("utf8")
    message_with_subject = "Subject: Amazon Price Alert! \n\n" + ''.join(message)

    # Send the email
    with smtplib.SMTP(SMTP_PROVIDER) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=os.environ.get("SMTP_PASSWORD"))
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=message_with_subject.encode("utf8"))


try:
    response = requests.get(PRODUCT_URL, headers=headers)
except requests.exceptions.RequestException as e:
    print(e)

if response:
    # Use BeautifulSoup to gather the price and product name.
    soup = BeautifulSoup(response.text, "html.parser")
    price_string = soup.find(class_="a-price-whole").text
    # Convert string to whole int.
    product_price = int(''.join([character for character in price_string if character.isdigit()]))
    product_name = soup.find(id="productTitle").text.strip()

    if product_price <= YOUR_MAX_PRICE:
        send_email(product_name, product_price)
