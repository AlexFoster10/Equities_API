from pydantic import BaseModel
from datetime import date as Date

class PriceResponse(BaseModel):
    ticker: str
    date: Date
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Config:
        from_attributes = True