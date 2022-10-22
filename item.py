import json


class Item:
    def __init__(self, date, price):
        self.date = date
        self.price = price

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
