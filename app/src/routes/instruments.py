from fastapi import APIRouter, HTTPException, Depends
from models.instrument import Instrument
from models.instrumentDB import InstrumentDB as ins_schema
from models.instrumentUpdate import InstrumentUpdate as ins_up
from models.instrumentResponse import InstrumentResponse as ins_re
import services.data_service as ds
from core.logger import get_logger
from typing import Optional
import pathlib, json
import sys
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
temp = pathlib.Path(__file__).parent.parent.parent.resolve().as_posix()
sys.path.append(temp)

router = APIRouter()
logger = get_logger()

#simple endpoint to return basic data
@router.get("/", response_model=list[ins_re])
async def get_instruments(db: Session = Depends(ds.get_db)):
    ins = db.query(ins_schema).all()
    return ins

#allows a user to search through instruments.json via any of the metrics
@router.get("/search")
async def search_instruments(
    sector: Optional[str] = None,
    exchange: Optional[str] = None,
    currency: Optional[str] = None,
    country: Optional[str] = None,
    instrument_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(ds.get_db)
):
    results = []

    ins = db.query(ins_schema).all()

    for i in ins:
        if sector and i.sector.lower() != sector.lower():
            continue
        if exchange and i.exchange.lower() != exchange.lower():
            continue
        if currency and i.currency.lower() != currency.lower():
            continue
        if country and i.country.lower() != country.lower():
            continue
        if instrument_type and i.instrument_type.lower() != instrument_type.lower():
            continue
        if is_active is not None and i.is_active != is_active:
            continue

        results.append(i)

    if not results:
        logger.info(f"Instrument not found")
        raise HTTPException(status_code=404, detail="Instrument not found")

    else:
        return results

#simple endpoint to return specific instrument
@router.get("/{ticker}", response_model=ins_re)
async def get_instruments(ticker = str, db: Session = Depends(ds.get_db)):
    ins = db.query(ins_schema).filter(ins_schema.ticker == ticker.upper()).first()

    if not ins:
        logger.info(f"Ticker could not be located: {ticker}")
        raise HTTPException(status_code=404, detail="Ticker not located")
    else:
        return ins

#allows a user to add instruments 
@router.post("/", response_model=ins_re, status_code=201)
async def create_instrument(new_instrument: Instrument, db: Session = Depends(ds.get_db)):

    try:
        ds.create_instrument_table()
        logger.info(f"Table doesn't exist, creating table")
    except:
        logger.info(f"Table exists")


    db_instrument = ins_schema(**new_instrument.model_dump())
    try:
        db.add(db_instrument)
        db.commit()
        db.refresh(db_instrument)
        return db_instrument
    except IntegrityError:
        logger.info(f"Ticker already exists")
        raise HTTPException(status_code=400, detail="Ticker already exists")

#allows a user to update existing instruments
@router.put("/{ticker}", response_model=ins_re, status_code=200)
async def update_instrument(ticker: str, instrument: ins_up, db: Session = Depends(ds.get_db)):
    db_ins = db.query(ins_schema).filter(ins_schema.ticker == ticker.upper()).first()

    if not db_ins:
        logger.info(f"Ticker could not be located: {ticker}")
        raise HTTPException(status_code=404, detail="Ticker not located")
    db_ins.ticker = instrument.ticker if instrument.ticker is not None else db_ins.ticker
    db_ins.company_name = instrument.company_name if instrument.company_name is not None else db_ins.company_name
    db_ins.exchange = instrument.exchange if instrument.exchange is not None else db_ins.exchange
    db_ins.currency = instrument.currency if instrument.currency is not None else db_ins.currency
    db_ins.sector = instrument.sector if instrument.sector is not None else db_ins.sector
    db_ins.country = instrument.country if instrument.country is not None else db_ins.country
    db_ins.instrument_type = instrument.instrument_type if instrument.instrument_type is not None else db_ins.instrument_type
    db_ins.is_active = instrument.is_active if instrument.is_active is not None else db_ins.is_active
    db.commit()
    db.refresh(db_ins)
    return db_ins

#allows a user to delete an item from instruments by ticker
@router.delete("/{ticker}", response_model=ins_re, status_code=200)
async def delete_instrument(ticker = str, db: Session = Depends(ds.get_db)):
    db_ins = db.query(ins_schema).filter(ins_schema.ticker == ticker.upper()).first()

    if not db_ins:
        logger.info(f"Ticker could not be located: {ticker}")
        raise HTTPException(status_code=404, detail="Ticker not located")
    db.delete(db_ins)
    db.commit()
    return db_ins
    
