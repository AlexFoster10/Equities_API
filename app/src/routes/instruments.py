from fastapi import APIRouter, HTTPException
from models.instrument import Instrument
import services.data_service as ds
from core.logger import get_logger
from typing import Optional
import pathlib, json
import sys
temp = pathlib.Path(__file__).parent.parent.parent.resolve().as_posix()
sys.path.append(temp)

instruments = ds.load_instruments()
prices = ds.load_prices()

router = APIRouter()
logger = get_logger()

#simple endpoints to return basic data
@router.get("/")
async def get_instruments():
    ins, pri = ds.load_tables_db()
    return ins

#allows a user to search through instruments.json via any of the metrics
@router.get("/search")
async def search_instruments(
    sector: Optional[str] = None,
    exchange: Optional[str] = None,
    currency: Optional[str] = None,
    country: Optional[str] = None,
    instrument_type: Optional[str] = None,
    is_active: Optional[bool] = None
):
    results = []

    ins, pri = ds.load_tables_db()

    for i in ins:
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
    
#allows a user to add instruments 
@router.post("/", response_model=Instrument, status_code=201)
async def create_instrument(new_instrument: Instrument):

    if " " in new_instrument.ticker:
        logger.error(f"Ticker is not valid: {new_instrument.ticker}")
        raise HTTPException(status_code=400, detail="Invalid ticker")

    try:
        for instrument in instruments:
            if instrument["ticker"].upper() == new_instrument.ticker.upper():
                logger.info(f"Ticker already exists: {new_instrument.ticker.upper()}")
                raise HTTPException(status_code=409, detail="Instrument with this ticker already exists")
        

        logger.info(f"Ticker created: {new_instrument.ticker.upper()}")
        instruments.append(new_instrument.model_dump())
        ds.save_instruments(instruments)
        return new_instrument
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error occurred while appending ticker: {str(e)}")
        raise HTTPException(status_code=500, detail="Bad request")
    
#allows a user to add instruments or edits existing instruments
@router.put("/{ticker}", response_model=Instrument, status_code=200)
async def update_instrument(ticker : str, new_instrument : Instrument):
    new_instrument.ticker = ticker
    if " " in ticker:
        logger.error(f"Ticker is not valid: {ticker}")
        raise HTTPException(status_code=400, detail="Invalid ticker")
    
    try:
        for instrument in instruments:
            if instrument["ticker"] == ticker:

                instruments.pop(instruments.index(instrument))
                instruments.append(new_instrument.model_dump())
                ds.save_instruments(instruments)
                logger.info(f"Instrument found with ticker, updated successfully: {ticker}")
                return new_instrument
        

        instruments.append(new_instrument.model_dump())
        ds.save_instruments(instruments)
        logger.info(f"Ticker could not be located, creating new entry: {ticker}")
        raise HTTPException(status_code=404, detail="Instrument not found, new entry created")
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error occurred while searching for/appending instrument with ticker: {ticker} - {str(e)}")
        raise HTTPException(status_code=500, detail="Bad request")
    
#allows a user to delete an item from instruments by ticker
@router.delete("/{ticker}", status_code=200)
async def delete_instrument(ticker : str):
    if " " in ticker:
        logger.error(f"Ticker is not valid: {ticker}")
        raise HTTPException(status_code=400, detail="Invalid ticker")
    
    try:
        for instrument in instruments:
            if instrument["ticker"] == ticker:

                deleted = instruments.pop(instruments.index(instrument))
                ds.save_instruments(instruments)
                logger.info(f"Instrument found with ticker, deleted successfully: {ticker}")
                return 

        logger.info(f"Ticker could not be located: {ticker}")
        raise HTTPException(status_code=404, detail="Bad request")
        
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error occurred while searching for instrument with ticker: {ticker} - {str(e)}")
        raise HTTPException(status_code=500, detail="Bad request")
    
##allows a user to retrieve an item by its ticker and display its price data
@router.get("/{ticker}/price",status_code=200)
@router.get("/{ticker}/prices",status_code=200)
async def get_price(ticker: str):

    if " " in ticker:
        logger.error(f"Ticker is not valid: {ticker}")
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