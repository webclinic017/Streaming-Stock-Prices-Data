# load package to extract stock data
import requests
from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient

today = date.today()

stockdata = []

def stock_extract(symbol):  # define function to extract stock data

    """
    Function extracts stock data from yahoo finance website.
    :param symbol: Input stock symbol
    :return: Returns a dictionary of stock information defined (Name, Symbol, Price, Change, time and date extracted)
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    url = f'https://ca.finance.yahoo.com/quote/{symbol}'  # url template to extract data

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    stock = {
        'fullname': soup.title.text.split('(')[0],  # Scraps the full name of the stock
        'symbol': symbol,
        # Scrap the price of the stock
        'price': soup.find('fin-streamer', {'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text,
        # Scrap the change in stock price (amount and percentage)
        'change': soup.find('fin-streamer', {'Fw(500) Pstart(8px) Fz(24px)'}).find_all('span')[0].text
                  + " " + soup.find('div', {'D(ib) Mend(20px)'}).find_all('span')[1].text,
        'time': soup.find('div', {'id':'quote-market-notice'}).text,
        'date extracted': today.strftime("%Y-%m-%d")
        }   # Dictionary template to reference the data
    return stock

def iterator(list):  # define a function to iterate through the list. we need this to build DAGs later.
    """
    This function extracts stock information from a list of stock symbols
    :param list: A list of stock symbols
    :return: Dictionary list of stock information
    """
    for i in list:
        stockdata.append(stock_extract(i))
        print('Extracting: ', i)


def load(dataset):
    """
    Loads the stock data into the mongo DB atlas database
    :return: No returned response
    """
    client = MongoClient(
        "mongodb+srv://dbuser:password1234@cluster0.gq30y.mongodb.net/Stocks?retryWrites=true&w=majority")
    db = client.Stocks
    stock1 = db.Stockdata
    stock1.insert_many(dataset)


# Get a list of the symbols of the most active stocks
stockstomonitor = ['NUG.V', 'SU.TO', 'HALO.NE', 'C.V', 'SCRN.CN', 'GWO.TO', 'NCU.TO', 'SLF.TO', 'TD.TO', 'EPY.CN',
                   'CVE.TO', 'ARX.TO', 'TKX.V', 'BNS.TO', 'VXTR.V', 'GHG.CN', 'HUT.TO', 'CNQ.TO', 'BTO.TO', 'ENB.TO',
                   'BB.TO', 'BTE.TO', 'GBLC.CN', 'ABX.TO', 'CM.TO']

# Write the pipeline

try:
    iterator(stockstomonitor)
except:
    print("An exception has occured")
else:
    print("Successfully extracted stock data ")


try:
    load(stockdata)
except:
    print("Load to Mongo DB failed")
else:
    print("load successful and connection closed!!!")

