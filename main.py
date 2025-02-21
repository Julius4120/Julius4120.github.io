import requests
import os
from twilio.rest import Client


# Case study is TESLA
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key = "DWR274ZBNR0MV61Y"

acct_sid = os.environ.get("ovm_acct_sid")

auth_token = os.environ.get("ovm_auth_token")
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


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


def percentage_calc() :
    diff = yesterday - day_before
    percentage = abs(round((diff / day_before) * 100, 3))
    return percentage # Percentage



# Getting stock prices of previous day from alphavantage
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key,
}
resource = requests.get(url = "https://www.alphavantage.co/query", params = parameters)
resource.raise_for_status()

data = resource.json()["Time Series (Daily)"]

my_data = [value for (index, value) in data.items()]
time = [index for (index, value) in data.items()]
yesterday = float(my_data[0]["4. close"])
day_before = float(my_data[1]["4. close"])




#Getting latest stock news on newsapi
parameters = {
    "apiKey": "c09f459375e249fea7f72d57a0ae4da6",
    "q": COMPANY_NAME,
    "language":"en",
    "from": time[5],
}
news_resource = requests.get(url="https://newsapi.org/v2/everything", params=parameters)
news_resource.raise_for_status()
news_data = news_resource.json()



# Main body of program
if percentage_calc() > 2 :
    if yesterday > day_before:  # Increase in stock
        sms_message = (f"\n{STOCK}🔺{percentage_calc()}%\n"
                       f"Title: {news_data["articles"][-1]["title"]}\n"
                       f"Brief: {news_data["articles"][-1]["content"]}")

        print("aa")


    else :  # Decrease in stock
        sms_message = (f"\n{STOCK}🔻{percentage_calc()}%\n"
                       f"Title: {news_data["articles"][-1]["title"]}\n"
                       f"Brief: {news_data["articles"][-1]["content"]}")



    # Using twilio api to send sms
    my_client = Client(acct_sid, auth_token)
    message = my_client.messages.create(
        body=sms_message,
        from_="+16206229217",
        to="+2349160707115",
    )
    print(message.status)
    print("sms sent successfully")









