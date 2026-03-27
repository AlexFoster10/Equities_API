from fastapi import APIRouter, HTTPException, Depends
from models.price import Price
from models.priceDB import PriceDB as pri_schema
from models.priceUpdate import PriceUpdate as pri_up
from models.priceResponse import PriceResponse as pri_re
import services.data_service as ds
from core.logger import get_logger
import pathlib
import sys
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
temp = pathlib.Path(__file__).parent.parent.parent.resolve().as_posix()
sys.path.append(temp)

router = APIRouter()
logger = get_logger()

#simple endpoint to return basic data
@router.get("/", response_model=list[pri_re])
async def get_price(db: Session = Depends(ds.get_db)):

    try:
        ds.create_prices_table()
        logger.info(f"Table doesn't exist, creating table")
    except:
        logger.info(f"Table exists")


    pri = db.query(pri_schema).all()
    return pri

#allows a user to add prices 
@router.post("/", response_model=pri_re, status_code=201)
async def create_price(new_price: Price, db: Session = Depends(ds.get_db)):

    try:
        ds.create_prices_table()
        logger.info(f"Table doesn't exist, creating table")
    except:
        logger.info(f"Table exists")


    db_price = pri_schema(**new_price.model_dump())
    try:
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price
    except IntegrityError:
        logger.info(f"Ticker with date already exists")
        raise HTTPException(status_code=400, detail="Ticker with date already exists")


            
    
