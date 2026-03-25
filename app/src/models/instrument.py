from pydantic import BaseModel

class Instrument(BaseModel):
    ticker: str
    company_name: str
    exchange: str
    currency: str
    sector: str
    country: str
    instrument_type: str
    is_active: bool