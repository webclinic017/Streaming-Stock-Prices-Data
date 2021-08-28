# load package to extract stock data
import requests
from bs4 import BeautifulSoup

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
        'symbol': symbol,
        'price': soup.find('div', {'D(ib) Mend(20px)'}).find_all('span')[0].text,
        'change': soup.find('div', {'D(ib) Mend(20px)'}).find_all('span')[1].text
        }   # Dictionary template to reference the data
    return stock


def iterator(list):  # define a function to iterate through the list. we need this to build DAGs later.
    for i in list:
        stockdata.append(stock_extract(i))
        print('Extracting: ', i)


iterator(stockstomonitor)

print(stockdata)






