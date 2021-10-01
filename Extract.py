# load package to extract stock data
import requests
from bs4 import BeautifulSoup
from datetime import date


today = date.today()


# Get a list of the symbols of the most active stocks
stockstomonitor = ['NUG.V', 'SU.TO', 'HALO.NE', 'C.V', 'SCRN.CN', 'GWO.TO', 'NCU.TO', 'SLF.TO', 'TD.TO', 'EPY.CN',
                   'CVE.TO', 'ARX.TO', 'TKX.V', 'BNS.TO', 'VXTR.V', 'GHG.CN', 'HUT.TO', 'CNQ.TO', 'BTO.TO', 'ENB.TO',
                   'BB.TO', 'BTE.TO', 'GBLC.CN', 'ABX.TO', 'CM.TO']

stockdata = []  # define empty list to collect stock data



def stock_extract(symbol):   # define function to extract stock data

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    url = f'https://ca.finance.yahoo.com/quote/{symbol}'  # url template to extract data

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    stock = {
        'fullname': soup.title.text.split('(')[0],
        'symbol': symbol,
        'price': soup.find('div', {'D(ib) Mend(20px)'}).find_all('span')[0].text,
        'change': soup.find('div', {'D(ib) Mend(20px)'}).find_all('span')[1].text,
        'time': soup.find('div', {'id':'quote-market-notice'}).text,
        'date extracted': today.strftime("%d/%m/%Y")
        }   # Dictionary template to reference the data
    return stock


def iterator(list):  # define a function to iterate through the list. we need this to build DAGs later.
    for i in list:
        stockdata.append(stock_extract(i))
        print('Extracting: ', i)


iterator(stockstomonitor)


print(stockdata)

import pymongo
from pymongo import MongoClient

# create client connection
client = MongoClient('mongodb+srv://dbuser:'
                     'password1234@cluster0.gq30y.mongodb.net/Stocks?retryWrites=true&w=majority')

# Assign database
db = client.Stocks

# link collection
stock1 = db.Stockdata

# insert data into database
stock1.insert_many(stockdata)

latest_stocks = stock1.find(
        filter={"date extracted": today.strftime("%d/%m/%Y")},
        projection={"symbol": 1, "price": 1, "change": 1, "_id": 0},  # fields that will be displayed
        sort=[("fullname", 1)]  # sort by full name, ascending order
    )

a = list(latest_stocks)


# obtain most up-to-date extraction date

sorted = stock1.find(
    filter={},
    projection={"_id": 0, "date extracted": 1},  # Select just the 'date extracted' field.
    sort=[("date extracted", -1)],  # Sort in descending order by 'date extracted'
).limit(1)  # limit to just one result

list_latest_date = list(sorted)  # convert to list

# Convert list to dictionary

latest_date={}
for i in list_latest_date:
    latest_date.update(i)

latest_stocks = stock1.find(
        filter=latest_date,
        projection={"symbol": 1, "price": 1, "change": 1, "_id": 0},  # fields that will be displayed
        sort=[("fullname", 1)]  # sort by full name, ascending order
    )
print(list(latest_stocks))


print(b)

print(a)


sample = [{'Name':'Tayo','Class':'primary 2'}, {'Name':'Shola','Class':'primary 2'}, {'Name':'John','Class':'primary 2'}]

int = []
full = ''
for x in sample:
    int.append(" | " + x['Name'] + " " + x['Class'])
for y in int:
    full += y



