import requests
import smtplib
import random
import math
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# STOCK PRICES API
API_KEY = "9RMQYPVC0KY4KCDL"
API = "https://www.alphavantage.co/query"

email = "oskar.lab16@gmail.com"
password = "zfdfqxxfjfcdvtta"

#NEWS API
API_KEY_2 = "18e9a45ed134434c9d1485c479d475ff"
API_2 = "https://newsapi.org/v2/everything"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": API_KEY,
}

response = requests.get(API, params=parameters)
response_json = response.json()
specific_day = response_json["Time Series (Daily)"]
new_list = [value for (key, value) in specific_day.items()]
dates_list = [key for (key, value) in specific_day.items()]

yesterday_data = new_list[0]
yesterday_closing_price = yesterday_data["4. close"]

before_data = new_list[1]
before_closing_price = before_data["4. close"]
before_real_date = dates_list[1]

print(f"Yesterday's price is {yesterday_closing_price}, but the price before yesterday: {before_closing_price}")

difference_between_days = abs(float(yesterday_closing_price) - float(before_closing_price))
print(difference_between_days)

difference_in_percents = (difference_between_days / float(yesterday_closing_price)) * 100
difference_to_display = math.ceil(difference_in_percents)
print(f"{difference_in_percents}%")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

if difference_in_percents > 5 or difference_in_percents < 5:
    if yesterday_closing_price > before_closing_price:
        symbol = "Growth"
    elif yesterday_closing_price < before_closing_price:
        symbol = "Loss"

    news_params = {
        "apiKey": API_KEY_2,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(API_2, params=news_params)
    news_json = news_response.json()["articles"]

    three_articles = news_json[:3]

    new_dictionary = {}
    number = 1

    for item in three_articles:
        new_dictionary[f"author{number}"] = item["author"]
        new_dictionary[f"title{number}"] = item["title"]
        new_dictionary[f"description{number}"] = item["description"]
        number += 1

    with smtplib.SMTP("smtp.gmail.com") as connection:
        random_number = random.randint(1, 3)
        random_author = new_dictionary[f"author{random_number}"]
        random_title = new_dictionary[f"title{random_number}"]
        random_descript = new_dictionary[f"description{random_number}"]

        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email, to_addrs="oskarkrawczyk14@gmail.com",
                            msg=f"Subject: {COMPANY_NAME} - {difference_to_display}% {symbol}\n\n{random_title}\n{random_descript}")
else:
    pass




## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

