import requests
import os
from twilio.rest import Client

# Company details to track
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# API keys
AA_API_KEY = os.environ['AA_API_KEY']
NEWS_API_KEY = os.environ['NEWS_API_KEY']
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

# Numbers
TWILIO_NUMBER = "0123456789"
YOUR_NUMBER = "0123456789"


def get_past_two_closing_rates():
    aa_request_params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK,
        "apikey": AA_API_KEY
    }

    aa_url = "https://www.alphavantage.co/query"
    request = requests.get(aa_url, params=aa_request_params)
    aa_data = request.json()

    # Yesterday and day before in YMD format
    yesterday = list(aa_data['Time Series (Daily)'])[0]
    before_yesterday = list(aa_data['Time Series (Daily)'])[1]

    # Closing prices as floats
    rate_yesterday = float(aa_data['Time Series (Daily)'][yesterday]['4. close'])
    rate_before_yesterday = float(aa_data['Time Series (Daily)'][before_yesterday]['4. close'])

    return {"yesterday": rate_yesterday, "before_yesterday": rate_before_yesterday}


def get_news():
    news_request_params = {
        "apiKey": NEWS_API_KEY,
        "q": "Tesla",
    }

    news_url = "https://newsapi.org/v2/everything"
    news_request = requests.get(news_url, params=news_request_params)
    # Get the first three articles and format them with line breaks
    news_data = news_request.json()['articles'][:3]
    articles = " ".join([f"Source: {article['source']['Name']}\n Brief: {article['title']}\n" for article in news_data])
    return articles


def send_twilio_message(change_in_percent, news, rates_gone_up):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message_body = ""

    if rates_gone_up:
        message_body = f"TSLA: 🔺{int(change_in_percent)}%\n {news}"
    else:
        message_body = f"TSLA: 🔻{int(change_in_percent)}%\n {news}"

    message = client.messages \
        .create(
        body=message_body,
        from_=TWILIO_NUMBER,
        to=YOUR_NUMBER,
    )


# Run once a day to check the stock exchange

# Get the closing rates of the past 2 days
closing_rates = get_past_two_closing_rates()

# Check to see if they went up or down
has_gone_up = closing_rates["yesterday"] > closing_rates["before_yesterday"]

# Calculate the percentage
difference = abs(closing_rates["yesterday"]) - abs(closing_rates["before_yesterday"])
difference_in_percent = (difference / closing_rates["yesterday"]) * 100

# If rates have gone up by 5% send message to phone with the latest news
if difference_in_percent > 5:
    send_twilio_message(difference_in_percent, get_news(), has_gone_up)
