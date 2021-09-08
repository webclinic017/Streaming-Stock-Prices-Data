import flask
from flask import request, jsonify, render_template
from pymongo import MongoClient
import datetime


# Connect to database, assign database and collection
conn_string = 'mongodb+srv://dbuser:password1234@cluster0.gq30y.mongodb.net/Stocks?retryWrites=true&w=majority'
client = MongoClient(conn_string)
db = client.Stocks
stock1 = db.Stockdata

# obtain most up-to-date extraction date
sorted = stock1.find(
    filter={},
    projection={"_id": 0, "date extracted": 1},  # Select just the 'date extracted' field.
    sort=[("date extracted", -1)],  # Sort in descending order by 'date extracted'
).limit(1)  # limit to just one result

list_latest_date = list(sorted)  # convert iteratable object to list

# Convert list to dictionary
latest_date={}
for i in list_latest_date:
    latest_date.update(i)

# Convert latest date string to date object
lds=latest_date['date extracted']  # extract date from dictionary

ldo=datetime.datetime.strptime(lds, "%d/%m/%Y").date()  # convert to date object
ldts=ldo.strftime("%A %B %d, %Y")



app = flask.Flask(__name__)
app.config["DEBUG"] = True  # starts debugger, helps refresh the webpage when code changes.

@app.route('/', methods=['GET'])  # Routing syntax to map URL '/' to create the landing page
def home():
    return '''<h1> Stock streaming web app</h1>
            <p>A sample webapp to display select stock information from the most active 25 sites</p>'''

@app.route('/api/stocks', methods=['GET'])  # Return all of the latest stocks (scrapped today)
def stocks_all():
    latest_stocks = stock1.find(
        filter=latest_date,
        projection={"symbol": 1, "price": 1, "change": 1, "_id": 0},  # fields that will be displayed
        sort=[("fullname", 1)]  # sort by track views, descending order
    )
    return jsonify(list(latest_stocks))

@app.route('/table/stocks', methods=['GET'])  # Return tabular data and ticker
def tabular():
    tabular_stocks = stock1.find(
        filter=latest_date,
        projection={"fullname": 1,"symbol": 1, "price": 1, "change": 1, "time": 1,  "_id": 0},  # fields that will be displayed
        sort=[("fullname", 1)]  # sort by track views, descending order
    )

    ticker = stock1.find(
        filter=latest_date,
        projection={"symbol": 1, "price": 1, "change": 1, "_id": 0},  # fields that will be displayed
        sort=[("fullname", 1)]  # sort by track views, descending order
    )

    return render_template('table.html', tabular_stocks=tabular_stocks, latest_date=ldts, ticker=list(ticker))


app.run()

