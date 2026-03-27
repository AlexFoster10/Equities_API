from fastapi import FastAPI, Response, status, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
import pathlib, json
import sys
import logging
from core.logger import get_logger
import services.data_service as ds 
from models.instrument import Instrument
from routes.instruments import router as INS
from routes.prices import router as PRI
temp = pathlib.Path(__file__).parent.parent.resolve().as_posix()
sys.path.append(temp)
app = FastAPI()
logger = get_logger()

#include additional routers
app.include_router(INS, prefix="/instruments", tags=["Instruments"])
app.include_router(PRI, prefix="/prices", tags=["Prices"])


#simple endpoints to return basic data
@app.get("/")
async def root():
    return {"message": "Hello World"}

