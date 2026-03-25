import json, sqlite3, pathlib, sys
import pathlib, json, sys
import pandas as pd
from fastapi import APIRouter, HTTPException

from core.logger import get_logger
from models.instrument import Instrument

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
        ins_df = pd.read_sql_query("SELECT * FROM Instruments",conn)
        
        ins_dict = ins_df.to_dict(orient='records')
        for ins in ins_dict:
            ins['is_active'] = bool(ins['is_active'])

        pri_df = pd.read_sql_query("SELECT * FROM Prices", conn)
        pri_dict = pri_df.to_dict(orient='records')
        conn.close()
        

        return ins_dict, pri_dict
    except Exception as e:
        logger.error(f"Error loading the database: {e}")
        return [],[]

data = {"ticker": "TestNewTickerAgain", 
         "company_name": "Apple Inc.", 
         "exchange": "NASDAQ", 
         "currency": "USD", 
         "sector": "Technology", 
         "country": "USA", 
         "instrument_type": "Equity", 
         "is_active": True}

def add_entry_instrument_db(entry : Instrument):
    try:
        conn = sqlite3.connect("app/data/equities.db", timeout=10)
        cursor = conn.cursor()
        # Extract and cast values to safe types
        ticker = entry.ticker.strip().upper()
        company_name = entry.company_name
        exchange = entry.exchange
        currency = str(entry.currency)  # if Currency is an Enum
        sector = entry.sector
        country = entry.country
        instrument_type = entry.instrument_type
        is_active = int(entry.is_active)  # True -> 1, False -> 0

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
            return 0
        else:
            logger.info(f"Successfully appended to Instruments table")
            return 1
    except Exception as e:
        logger.error(f"Error occurred while appending to Instruments table: {str(e)}")
        

