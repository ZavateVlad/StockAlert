import requests
from twilio.rest import Client
import credentials

STOCK_API = "https://www.alphavantage.co/query"
NEWS_API = "https://newsapi.org/v2/everything"

STOCK = "IBM"


def get_news_data():
    news_list = []
    parameters = {
        'qInTitle': STOCK,
        'language': 'en',
        'sortBy': 'popularity',
        'apikey': credentials.news_api,
    }

    response = requests.get(url='https://newsapi.org/v2/everything', params=parameters)
    data = response.json()['articles']
    three_articles = data[:3]

    for article in three_articles:
        news_dictionary = {'title': article['title'], 'brief': article['description'], 'url': article['url']}
        news_list.append(news_dictionary)
    return news_list


def get_stock_data():
    parameters = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': STOCK,
        'apikey': 'demo',  # Using demo api key, there can be unlimited requests
    }

    response = requests.get(url='https://www.alphavantage.co/query', params=parameters)

    data = response.json()['Time Series (Daily)']
    days_data = [value for (key, value) in data.items()]
    yesterday_data = days_data[0]
    day_before_yesterday_data = days_data[1]

    yesterday_closing = yesterday_data['4. close']
    day_before_yesterday_closing = day_before_yesterday_data['4. close']

    difference = float(yesterday_closing) - float(day_before_yesterday_closing)
    percentage = round((difference / float(yesterday_closing)) * 100, 2)
    return f"{STOCK}: {percentage}%"


def get_phone_msg():
    news = get_news_data()
    stock_percentage = get_stock_data()
    email_body = f"{stock_percentage}\n"

    for article in news:
        email_body += f"Headline: {article['title']}\n"
        email_body += f"Brief: {article['brief']}\n"
        email_body += f"Url: {article['url']}\n"

    client = Client(credentials.Twilio_sid, credentials.Twilion_auth_token)
    message = client.messages. \
        create(
            body=email_body,
            from_='+17868414552',
            to='+40 730 215 709'
        )

    print(message.status)


get_phone_msg()
