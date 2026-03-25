from fastapi import FastAPI, Response, status, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
import pathlib, json
import sys
import logging
from src.core.logger import get_logger
import src.services.data_service as ds 
from src.models.instrument import Instrument
import src.routes.instruments as INS
temp = pathlib.Path(__file__).parent.parent.resolve().as_posix()
sys.path.append(temp)
app = FastAPI()
logger = get_logger()

#load file data into variables
instruments = ds.load_instruments()
prices = ds.load_prices()

app.include_router(INS.router, prefix="/instruments", tags=["Instruments"])

#simple endpoints to return basic data
@app.get("/")
async def root():
    return {"message": "Hello World"}

