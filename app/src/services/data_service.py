import json, sqlite3, pathlib, sys
import pathlib, json, sys
import pandas as pd
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from core.logger import get_logger
from models.instrument import Instrument
from models.instrumentDB import Base
from models.instrumentDB import InstrumentDB as ins_schema
logger = get_logger()



INSTRUMENTS_FILE = "app/data/instruments.json"
PRICES_FILE = "app/data/prices.json"
DB_FILE = "sqlite:///app/data/equities.db"

engine = create_engine(DB_FILE, connect_args={"check_same_thread": False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
    

def create_instrument_table():
    Base.metadata.create_all(bind=engine)






     
    

    
        

