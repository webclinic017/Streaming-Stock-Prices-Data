import flask
from flask import request, jsonify, render_template
from pymongo import MongoClient
import datetime

app = flask.Flask(__name__)

ENV = "DEV"
if ENV == "DEV":
    app.config["DEBUG"] = True
    client = MongoClient('mongodb+srv://dbuser:password1234@cluster0.gq30y.mongodb.net/Stocks?retryWrites=true&w=majority')
else:
    app.config["DEBUG"] = False
    client = MongoClient('mongodb+srv://dbuser:password1234@cluster0.gq30y.mongodb.net/Stocks?retryWrites=true&w=majority')

# Connect to database, assign database and collection
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

@app.route('/', methods=['GET'])  # Routing syntax to map URL '/' to create the landing page
def home():
    return '''<h1> Stock streaming web app</h1>
            <p>A sample webapp to display select stock information from the most active 25 sites</p>'''

@app.route('/api', methods=['GET'])  # Return all of the latest stocks (scrapped today) to an api
def stocks_all():
    latest_stocks = stock1.find(
        filter=latest_date,
        projection={"symbol": 1, "price": 1, "change": 1, "_id": 0},  # fields that will be displayed
        sort=[("fullname", 1)]  # sort by track views, descending order
    )
    return jsonify(list(latest_stocks))

@app.route('/table', methods=['GET'])  # Return tabular data and ticker
def tabular():
    tabular_stocks = stock1.find(
        filter=latest_date,
        projection={"fullname": 1, "symbol": 1, "price": 1, "change": 1, "time": 1,  "_id": 0},  # fields to be displayed
        sort=[("fullname", 1)]  # sort by track views, descending order
    )

    ticker = stock1.find(
        filter=latest_date,
        projection={"symbol": 1, "price": 1, "change": 1, "_id": 0},  # fields that will be displayed
        sort=[("fullname", 1)]  # sort by track views, descending order
    )

    int_t = []  # create empty list for the intermediate ticker
    full_t = ''  # create empty string for final ticker
    for x in ticker:
            int_t.append(" | " + x['symbol'] +
                         "  " + x['price'] + " " + x['change'])  # create ticker to show stock symbol, change and price.
    for values in int_t:
        full_t += values  # collapse ticker into a full string

    return render_template('table.html', tabular_stocks=tabular_stocks, latest_date=ldts, ticker=full_t)


if __name__ == "__main__":  # I am not sure of what this does, but it enables Gunicorn run the app.
    app.run()


