from flask import json, jsonify
import requests
from bs4 import BeautifulSoup, Tag
from item import Item
import datetime
from typing import List
from threading import Thread

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
    items = []
    num = getPageNumbers(1, country, searchText)

    threads = []
    for i in range(num):
        pageThread = Thread(target=getPage, args=(items, pageNo, country, searchText))
        pageThread.start()
        threads.append(pageThread)
        pageNo += 1

    for t in threads:
        t.join()
    # for i in items:
    #     print(i.date)
    print(f"num items {len(items)}")
    print(f"num pages {num}")
    return json.dumps([ob.__dict__ for ob in items])


def getPageNumbers(pageNo, country, searchText):
    url = f"https://www.ebay.com.{country}/sch/i.html?_from=R40&_nkw={searchText}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=3000&_sargn=-1%26saslc%3D1&_salic=15&_sop=12&_dmd=1&_ipg=240&LH_Complete=1&_pgn={pageNo}"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    li = soup.find("h1", {"class": "srp-controls__count-heading"})

    assert isinstance(li, Tag)
    children = li.findChildren("span", recursive=False)

    return 1 + (int(children[0].contents[0].replace(",", "")) // 240)
    # for child in children:
    #     print(child.contents())


def getPage(items, pageNo, country, searchText):
    url = f"https://www.ebay.com.{country}/sch/i.html?_from=R40&_nkw={searchText}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=3000&_sargn=-1%26saslc%3D1&_salic=15&_sop=12&_dmd=1&_ipg=240&LH_Complete=1&_pgn={pageNo}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    priceAndDateList = soup.findAll("span", {"class": "POSITIVE"})

    price = 0
    date = datetime.datetime.now()

    if len(priceAndDateList) == 0:
        return None
    page = []
    for span in priceAndDateList:
        line = span.contents[0]
        if "to" in line:
            continue

        if "Sold" not in line:
            try:
                price = float(line.split(" ")[1][1:].replace(",", ""))
            except:
                print(line)

            print(price)

            page.append(Item(date.strftime("%d-%m-%Y"), price))
        else:
            dates = line[6:].split()
            print(dates)
            date = datetime.datetime(int(dates[2]), dateMap[dates[1]], int(dates[0]))

    print(url)
    items += page

def getAveragePerDay(searchText, country)
