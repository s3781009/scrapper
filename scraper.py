from flask import json, jsonify
import requests
from bs4 import BeautifulSoup
from item import Item
import datetime

dateMap = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def getPriceHistoryPage(searchText, country):
    pageNo = 1
    while True:
        url = f"https://www.ebay.com.{country}/sch/i.html?_from=R40&_nkw={searchText}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=3000&_sargn=-1%26saslc%3D1&_salic=15&_sop=12&_dmd=1&_ipg=240&LH_Complete=1&_pgn={pageNo}"
        pageNo += 1
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        priceAndDateList = soup.findAll("span", {"class": "POSITIVE"})

        if len(priceAndDateList) == 0:
            break

        items = []

        price = None
        date = None
        for span in priceAndDateList:
            line = span.contents[0]

            if "Sold" not in line:
                price = float(line.split(" ")[1][1:].replace(",", ""))
            else:
                dates = line[6:].split()
                date = datetime.datetime(
                    int(dates[2]), dateMap[dates[1]], int(dates[0])
                )
            items.append(Item(date, price))

    # for i in items:
    #     print(i.date)

    return jsonify([u.to_json() for u in items])
