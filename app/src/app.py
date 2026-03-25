from fastapi import FastAPI, Response, status, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
import pathlib, json
import sys
import logging
temp = pathlib.Path(__file__).parent.parent.parent.resolve().as_posix()
sys.path.append(temp)
app = FastAPI()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.FileHandler("app/testing/mainlog.log", mode="w")      
handler.setFormatter(formatter)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class Instrument(BaseModel):
    ticker: str
    company_name: str
    exchange: str
    currency: str
    sector: str
    country: str
    instrument_type: str
    is_active: bool


with open("app/data/instruments.json") as f:
    instruments = json.load(f)
    instruments = instruments["instruments"]

with open("app/data/prices.json") as f:
    prices = json.load(f)
    prices = prices["prices"]


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/instruments")
async def get_instruments():
    return instruments

@app.get("/instruments/price")
@app.get("/instruments/prices")
async def get_prices():
    return prices

@app.get("/instruments/search")
async def search_instruments(
    sector: Optional[str] = None,
    exchange: Optional[str] = None,
    currency: Optional[str] = None,
    country: Optional[str] = None,
    instrument_type: Optional[str] = None,
    is_active: Optional[bool] = None
):
    results = []

    for i in instruments:
        if sector and i["sector"].lower() != sector.lower():
            continue
        if exchange and i["exchange"].lower() != exchange.lower():
            continue
        if currency and i["currency"].lower() != currency.lower():
            continue
        if country and i["country"].lower() != country.lower():
            continue
        if instrument_type and i["instrument_type"].lower() != instrument_type.lower():
            continue
        if is_active is not None and i["is_active"] != is_active:
            continue

        results.append(i)

    if not results:
        logger.info(f"Instrument not found")
        raise HTTPException(status_code=404, detail="Instrument not found")

    else:
        return results

@app.post("/instruments", response_model=Instrument, status_code=201)
async def create_instrument(new_instrument: Instrument):
    # 1. Check for duplicates
    try:
        for instrument in instruments:
            if instrument["ticker"].upper() == new_instrument.ticker.upper():
                logger.info(f"Ticker already exists: {new_instrument.ticker.upper()}")
                raise HTTPException(status_code=409, detail="Instrument with this ticker already exists")
        
        # 2. Add to dataset
        instruments.append(new_instrument.model_dump())
        with open("app/data/instruments.json", "w") as f:
            json.dump(instruments, f)
        return new_instrument
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error occurred while appending ticker: {str(e)}")
        raise HTTPException(status_code=500, detail="Bad request")

    # 3. Return the created instrument
    

@app.get("/instruments/{ticker}",status_code=200)
async def get_instrument(ticker: str):

    if not ticker.isalpha():
        logger.error(f"Ticker is not alphabetical: {ticker}")
        raise HTTPException(status_code=400, detail="Invalid ticker")
    
    try:
        for instrument in instruments:
            if instrument["ticker"] == ticker:
                logger.info(f"Instrument found with ticker: {ticker}")
                return instrument
        logger.error(f"Error occurred while searching for instrument with ticker: {ticker}")
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error occurred while searching for instrument with ticker: {ticker} - {str(e)}")
        raise HTTPException(status_code=500, detail="Bad request")

@app.get("/instruments/{ticker}/price",status_code=200)
@app.get("/instruments/{ticker}/prices",status_code=200)
async def get_price(ticker: str):

    if not ticker.isalpha():
        logger.error(f"Ticker is not alphabetical: {ticker}")
        raise HTTPException(status_code=400, detail="Invalid ticker")
    
    try:
        for price in prices:
            if price["ticker"] == ticker:
                logger.info(f"Price of ticker found: {ticker}: {price}")
                return price
        logger.error(f"Error occurred while searching for price of ticker: {ticker} :{price}")
        raise HTTPException(status_code=404, detail="Price not found")
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error occurred while searching for price of ticker: {ticker} :{price} - {str(e)}")
        raise HTTPException(status_code=500, detail="Bad request")




