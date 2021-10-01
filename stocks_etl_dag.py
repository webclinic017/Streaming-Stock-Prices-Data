from airflow.models import DAG
from airflow.operators.python_operators import PythonOperator
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime

today = date.today()

stockdata = []

# Define default arguments

default_arguments = {
    'owner': 'Ameen',
    'email': ['alameenshifatu@yahoo.com'],
    'start_date': datetime(2021, 10, 3),
    'retries': 3
}

stocks_etl_dag = DAG('stock_etl_workflow',
                     default_args=default_arguments, schedule_interval='30 16 * * 1,2,3,4,5')  # scheduled to run at 4:30 every monday to friday


def iterator(list):
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
    for i in list:
        stockdata.append(stock_extract(i))
        print('Extracting: ', i)


stocks_extract_transform = PythonOperator(
    task_id= 'Extract&transform',
    python_callable=iterator,
    
)