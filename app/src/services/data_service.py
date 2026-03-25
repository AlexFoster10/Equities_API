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
    try:
        conn = sqlite3.connect("app/data/equities.db")
        ins = pd.read_sql_query("SELECT * FROM Instruments",conn)
        pri = pd.read_sql_query("SELECT * FROM Prices",conn)
        print(ins.to_string())
        print(pri.to_string())
        return ins, pri
    except Exception as e:
        logger.error(f"Error loading the database: {e}")
        return

data = {"ticker": "AAadswPL", 
         "company_name": "Apple Inc.", 
         "exchange": "NASDAQ", 
         "currency": "USD", 
         "sector": "Technology", 
         "country": "USA", 
         "instrument_type": "Equity", 
         "is_active": True}

def add_entry_ins_db(entry):
    try:
        conn = sqlite3.connect("app/data/equities.db")
        entry = pd.json_normalize(entry)
        entry.to_sql("Instruments", conn, if_exists='append', index= False)
        conn.close()
        logger.info(f"Successfully appended to Instruments table")
    except Exception as e:
        logger.error(f"Error occurred while appending to Instruments table: {str(e)}")
        




def main():
    print(sys.path)
    load_tables_db()
    add_entry_ins_db(data)

if __name__ == "__main__":
    main()

