from pydantic import BaseModel
from datetime import date as Date
from typing import Optional

class PriceUpdate(BaseModel):
    ticker: Optional[str] = None       # optional, in case you allow PK update
    date: Optional[Date] = None        # optional, in case you allow PK update
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None