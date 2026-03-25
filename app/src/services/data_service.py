import json, sqlite3, pathlib, sys
import pathlib, json, sys
import pandas as pd

from app.src.core.logger import get_logger

logger = get_logger()

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


def load_tables_db():
    # try:
    #     conn = sqlite3.connect("app/data/equities.db")
    #     cur = conn.cursor()
    #     cmd = '''SELECT * FROM '''

    df = pd.read_json("app/data/instruments.json")
    df = pd.json_normalize(df["instruments"])
    try:
        conn = sqlite3.connect("app/data/equities.db")
        df.to_sql("Instruments", conn, if_exists='fail', index=False)
        logger.info(f"Data successfully added to equities in table Instruments")
        conn.close()
    except Exception as e:
        logger.error(f"Error loading the database: {e}")
        return


def main():
    print(sys.path)
    load_tables_db()

if __name__ == "__main__":
    main()

