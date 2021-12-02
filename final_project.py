import httplib2, urllib
import http.client
from time import localtime, strftime
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def thingspeak(price_bit,google_price,price_snapchat,amazon_price,apple_price,walmart_price):
    params = urllib.parse.urlencode({'field1': price_bit,'field2': google_price,'field4': price_snapchat,'field5': amazon_price, 'field6': apple_price, 'field7': walmart_price,'key': 'IDE76O025YB3X7CO'})
    headers = {"Content-type":
                   "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        conn.close()
        print("Upload Successfully")
    except:
        print("connection failed")

def get_price(w,y):

    r = requests.get(w)
    price_bit = BeautifulSoup(r.text, 'lxml')
    price_bit= price_bit.find('div', {"class" : y})
    price_bit = price_bit.find('span').text
    return price_bit

while True:
    print('Stocks prices')



    walmart_url= 'https://finance.yahoo.com/quote/WMT?p=WMT&.tsrc=fin-srch'
    y1 = 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)'
    walmart_price = get_price(walmart_url, y1)
    print('Price of Walmart: '+ str(float(walmart_price)))



    amazon_url = 'https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch'
    y2 = 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)'
    amazon_price = get_price(amazon_url,y2)
    print('Price of Amazon: ' + str(float(amazon_price)))

    apple_url = 'https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch'
    y3 = 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)'
    apple_price = get_price(apple_url, y3)
    print('Price of Apple: ' + str(float(apple_price)))

    bit_coin_url = 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch'
    y4 = 'My(6px) Pos(r) smartphone_Mt(6px) W(100%) D(ib) smartphone_Mb(10px) W(100%)--mobp'
    price_bit = get_price(bit_coin_url, y4)
    print('Price of bitcoin: ' + str(float(price_bit)))

    google_url = 'https://finance.yahoo.com/quote/GOOG?p=GOOG&.tsrc=fin-srch'
    y5 = 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)'
    price_google = get_price(google_url, y5)
    print('Price of Google: ' + str(float(price_google)))



    snapchat_url = 'https://finance.yahoo.com/quote/SNAP?p=SNAP&.tsrc=fin-srch'
    y7 = 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)'
    price_snapchat = get_price(snapchat_url, y7)
    print('Price of Snapchat: ' + str(float(price_snapchat)))


    thingspeak(price_bit,price_google,price_snapchat,amazon_price,apple_price,walmart_price)

    prices = [price_bit, price_google, price_snapchat, amazon_price, apple_price, walmart_price]

    prices_float = [float(i) for i in prices]
    prices_float_final = [format(datetime.now().date()), format(datetime.now().time())] + prices_float

    try:
        with open('stock_price.csv','a') as csv_file:
            csv.writer(csv_file).writerow(prices_float_final)
    except Exception as e:
        print("Couldn't write to the file due to "+ str(e))

    print("Twitting by thingtweet program")
    API_KEY = 'QWWMPUEZOKF7VEW8'
    url = "http://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key="
    fill = "&status="
    url = url + API_KEY + fill
    tweet = ('Bitcoin:''\n' +(price_bit)[0:7]+'\n'+'Google:''\n' +(price_google)+'\n''Snapchat:''\n'+(price_snapchat)+'\n''Amazon:''\n'+(amazon_price)+'\n''Apple:''\n'+(apple_price)+'\n''Walmart:''\n'+(walmart_price))
    url = url + tweet
    response = requests.get(url)
    if response.status_code == 200:
        print("Tweet sent")
    else:
        print ("tweet failed due to error=")
        print (response.status_code)

    time.sleep(30)

