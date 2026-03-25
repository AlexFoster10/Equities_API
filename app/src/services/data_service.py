import json

INSTRUMENTS_FILE = "app/data/instruments.json"
PRICES_FILE = "app/data/prices.json"

def load_instruments():
    with open(INSTRUMENTS_FILE) as f:
        instruments = json.load(f)
        instruments = instruments["instruments"]
        return instruments

def save_instruments(instruments):
    with open(INSTRUMENTS_FILE, "w") as f:
        json.dump({"instruments": instruments}, f)

def load_prices():
    with open(PRICES_FILE) as f:
        prices = json.load(f)
        prices = prices["prices"]
        return prices
    
def save_prices(prices):
    with open(PRICES_FILE, "w") as f:
        json.dump({"prices": prices}, f,  default=str)