import json
from datetime import date


class Item:
    def __init__(self, date: str, price: float):
        self.date = date
        self.price = price

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
