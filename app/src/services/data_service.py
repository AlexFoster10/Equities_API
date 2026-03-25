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
        conn.close()
        return ins, pri
    except Exception as e:
        logger.error(f"Error loading the database: {e}")
        return

data = {"ticker": "TestNewTickerAgain", 
         "company_name": "Apple Inc.", 
         "exchange": "NASDAQ", 
         "currency": "USD", 
         "sector": "Technology", 
         "country": "USA", 
         "instrument_type": "Equity", 
         "is_active": True}

def add_entry_ins_db(entry):
    for key, value in entry.items():
        print(f"{key}: {value} ({type(value)})")
    try:
        conn = sqlite3.connect("app/data/equities.db", timeout=10)
        cursor = conn.cursor()
        # Extract and cast values to safe types
        ticker = str(entry.get("ticker")).strip().upper()
        company_name = str(entry.get("company_name"))
        exchange = str(entry.get("exchange"))
        currency = str(entry.get("currency"))
        sector = str(entry.get("sector"))
        country = str(entry.get("country"))
        instrument_type = str(entry.get("instrument_type"))
        is_active = int(bool(entry.get("is_active")))  # True -> 1, False -> 0

        # Insert into SQLite
        cursor.execute("""
            INSERT OR IGNORE INTO Instruments
            (ticker, company_name, exchange, currency, sector, country, instrument_type, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticker, company_name, exchange, currency, sector, country, instrument_type, is_active))
        

        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            logger.info(f"Ticker already present in table")
        else:
            logger.info(f"Successfully appended to Instruments table")
    except Exception as e:
        logger.error(f"Error occurred while appending to Instruments table: {str(e)}")
        




def main():
    #load_tables_db()
    add_entry_ins_db(data)

if __name__ == "__main__":
    main()

