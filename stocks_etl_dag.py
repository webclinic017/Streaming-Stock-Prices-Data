from airflow import DAG
from airflow.operators.python_operators import PythonOperator
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import json

today = date.today()

stockdata = []

# list of the symbols of the most active stocks
stockstomonitor = ['NUG.V', 'SU.TO', 'HALO.NE', 'C.V', 'SCRN.CN', 'GWO.TO', 'NCU.TO', 'SLF.TO', 'TD.TO', 'EPY.CN',
                   'CVE.TO', 'ARX.TO', 'TKX.V', 'BNS.TO', 'VXTR.V', 'GHG.CN', 'HUT.TO', 'CNQ.TO', 'BTO.TO', 'ENB.TO',
                   'BB.TO', 'BTE.TO', 'GBLC.CN', 'ABX.TO', 'CM.TO']


def iterator(list):
    """function to iterate through the list"""

    def stock_extract(symbol):
        """define nested function to extract stock data"""

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        url = f'https://ca.finance.yahoo.com/quote/{symbol}'  # url template to extract data

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')
        stock = {
            'fullname': soup.title.text.split('(')[0],
            'symbol': symbol,
            'price': soup.find('div', {'D(ib) Mend(20px)'}).find_all('span')[0].text,
            'change': soup.find('div', {'D(ib) Mend(20px)'}).find_all('span')[1].text,
            'time': soup.find('div', {'id': 'quote-market-notice'}).text,
            'date extracted': today.strftime("%d/%m/%Y")
        }  # Dictionary template to reference the data
        return stock

    for i in list:
        stockdata.append(stock_extract(i))
        print('Extracting: ', i)
        with open('stocks.txt', 'w') as outfile:
            json.dump(stockdata, outfile)


def load(path):
    """load extracted stocks data unto mongodb database"""
    from pymongo import MongoClient
    with open(path) as json_file:
        df = json.load(json_file)
    client = MongoClient('mongodb+srv://dbuser:'
                         'password1234@cluster0.gq30y.mongodb.net/Stocks?retryWrites=true&w=majority')  # Define mongodb client
    db = client.Stocks  # assign database
    stock1 = db.Stockdata  # assign collection
    stock1.insert_many(df)  # insert dataframe into database and close connection


def remove_file(path):
    """Delete json file"""
    import os
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


# Define default arguments

default_arguments = {
    'owner': 'Ameen',
    'email': ['alameenshifatu@yahoo.com'],
    'start_date': datetime(2021, 10, 3),
    'retries': 2
}

with DAG(
        dag_id='stock_etl_workflow',
        default_args=default_arguments,
        schedule_interval='30 16 * * 1,2,3,4,5'  # scheduled to run at 4:30 every monday to friday
) as dag:

    ExtractTransform = PythonOperator(
        task_id='Extract&transform',
        python_callable=iterator,
        op_kwags={'list': stockstomonitor}
    )  # task 1. Extract and transform stock information. Save as a file

    LoadStocks = PythonOperator(
        task_id='LoadStocks',
        python_callable=load,
        op_kwags={'path': 'stocks.txt'}
    )  # task 2. load data into database

    DeleteFile = PythonOperator(
        task_id='DeleteFile',
        python_callable='remove_file',
        op_kwags={'path': 'stocks.txt'}
    )

    ExtractTransform >> LoadStocks >> DeleteFile

