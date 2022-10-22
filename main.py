from flask import Flask, request

from scraper import getPriceHistoryPage

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    search = request.args.get("search")
    country = request.args.get("country")
    res = getPriceHistoryPage(searchText=search, country=country)
    return res
