from pydantic import BaseModel, field_validator
from pydantic_extra_types.currency_code import Currency

#instrument class def
class Instrument(BaseModel):
    ticker: str
    company_name: str
    exchange: str
    currency: Currency
    sector: str
    country: str
    instrument_type: str
    is_active: bool

    @field_validator("ticker")
    @classmethod
    def no_spaces_in_ticker(cls, v):
        if " " in v:
            raise ValueError("Ticker must not contain spaces")
        return v