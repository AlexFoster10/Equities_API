from pydantic import BaseModel
from pydantic_extra_types.currency_code import Currency

class Instrument(BaseModel):
    ticker: str
    company_name: str
    exchange: str
    currency: Currency
    sector: str
    country: str
    instrument_type: str
    is_active: bool