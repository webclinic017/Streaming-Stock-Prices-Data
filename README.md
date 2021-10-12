## Streaming Stock Prices Data

This is a web application that streams stock prices data on a daily basis. It displays the current stock information about 25 stocks listed on the Toronto stock exchange.

See the attached link to the flask application: http://streamingstocks.herokuapp.com/

### How It Works

Using the diagram below, I am going to explain how the application works:

![Streaming1](https://user-images.githubusercontent.com/83844773/136867820-6b5bceae-24ad-4f4a-870d-d6022e2dc5df.png)

#### The Data layer:

This layer contains an ETL pipeline which sources data (from yahoo finance), transforms it and loads it to a mongodb atlas database. 
The ETL pipeline is orchestrated using Apache Airflow. The DAG for the pipeline is triggered around 4:30 pm EDT from Monday to Friday.
This is because the stock exchange closes after 4pm and does trade over the weekends. Hence, no data is generated during those times.

In the extraction phase of the pipeline, the stock prices for the relevant stocks is scrapped using the python package called Beautiful soup.
The data is then transformed into a python dictionary where the full name of the company, the stock symbol, the price, the change in price and the closing time is stored. 
The various dictionaries that represent each stock information are appended together and stored within a document store database (Mongodb atlas). 

#### Business logic layer

This layer dictates the various functionalities of the application. Using the flask package, we created the app to route GET requests from the mongodb database to various pages.
This application picks up the most up-to-date stock prices uploaded within the database and displays it within a table and an API.
The app was then deployed on Heroku, a PAAS that enables the deployment of applications in cloud. You can view the file labeled "api.py" within the repository for the code used.
#### Presentation layer

This represents the UI of the web app, where the user views and consumes the data.
The app is made up of 3 pages namely:
1) The landing page: https://streamingstocks.herokuapp.com/
2) The api (where users can download the daily data in json format): https://streamingstocks.herokuapp.com/api
3) The table (Where users can view the stocks within tables and as a ticker): https://streamingstocks.herokuapp.com/table

### Conclusion

This project gave me an opportunity to design and maintain an ETL pipeline using Airflow. It also gave me an opportunity to create and deploy a simple web application.
The application provides a window into the database, which is the final destination of the data flowing through the pipeline. 
Using this app, we can observe the quality and accuracy of the data being scrapped from yahoo finances which will also inform us that the pipeline works. 
