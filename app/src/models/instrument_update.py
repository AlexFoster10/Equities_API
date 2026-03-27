from pydantic import BaseModel
from pydantic_extra_types.currency_code import Currency
from typing import Optional

class Instrument_Update(BaseModel):
    ticker: Optional[str] = None
    company_name: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[Currency] = None
    sector: Optional[str] = None
    country: Optional[str] = None
    instrument_type: Optional[str] = None
    is_active: Optional[bool] = None