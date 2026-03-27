# from fastapi import APIRouter, HTTPException
# from models.instrument import Instrument
# from models.price import Price
# import services.data_service as ds
# from core.logger import get_logger
# from typing import Optional
# import pathlib, json
# import sys
# temp = pathlib.Path(__file__).parent.parent.parent.resolve().as_posix()
# sys.path.append(temp)

# instruments = ds.load_instruments()
# prices = ds.load_prices()

# router = APIRouter()
# logger = get_logger()

# #simple endpoints to return basic data
# @router.get("/")
# async def get_prices():
#     return prices

# @router.post("/",response_model=Price,status_code=201)
# async def create_price(new_price: Price):

#     try:
#         for x in prices:
#             if x["date"] == new_price.date:
#                 if x["ticker"].upper() == new_price.ticker.upper():
#                     logger.info(f"Error occurred while appending price, price with matchin ticker and date already exists: {str(e)}")
#                     raise HTTPException(status_code=409, detail="Instrument with this ticker already exists")
#                 else:
#                     logger.info(f"Price created: {new_price.ticker.upper()}")
#                     prices.append(new_price.model_dump())
#                     ds.save_prices(prices)
#                     return new_price
#         prices.append(new_price.model_dump())
#         ds.save_prices(prices)
#         return new_price  
#     except HTTPException:
#         raise

#     except Exception as e:
#         logger.error(f"Error occurred while appending price: {str(e)}")
#         raise HTTPException(status_code=500, detail="Bad request")


            
    
