from flask import Flask, request

from scraper import getPriceHistoryPage

app = Flask(__name__)

# Retrieve all the price information about a sold product unfiltered
@app.route("/all", methods=["GET"])
def getALl():
    search = request.args.get("search")
    country = request.args.get("country")
    res = getPriceHistoryPage(searchText=search, country=country)
    return res


@app.route("/dailyaverage", methods=["GET"])
def getDailyAverage():
    search = request.args.get("search")
    country = request.args.get("country")
    res = getAveragePerDay(searchText=search, country=country)
    return res
