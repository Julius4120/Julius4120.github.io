import requests
from bs4 import BeautifulSoup
import smtplib
email = email
password = password


headers = {
    'User-Agent': "*************",
    "Accept-Language": "********",
     "Accept-Encoding":"******************",
}
print("aaa")
response = requests.get(url="https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6", headers=headers)
print("bbb")
web_data = response.text

souppy = BeautifulSoup(web_data, "html.parser")

whole = souppy.find(name="span", class_="a-price-whole")
decimal = souppy.find(name="span", class_="a-price-fraction")
price = float(f"{whole.getText()}{decimal.getText()}")
title = souppy.select("#productTitle")
link = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
print(price)

if price < 100 :
    with smtplib.SMTP_SSL("smtp.gmail.com") as my_connection :
        my_connection.ehlo()
        my_connection.login(user=email, password=password)
        my_connection.sendmail(from_addr=email, to_addrs="opeayobello@gmail.com",
                               msg=f"Subject: PRICE ALERT\n\n{title} is \n\n now ${price}\n\n{link}")

