from pydantic import BaseModel, field_validator, model_validator
from pydantic_extra_types.currency_code import Currency
from datetime import date

class Price(BaseModel):
    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float

    @field_validator("open", "high", "low", "close", "volume")
    @classmethod
    def non_negative(cls, v, field):
        if v < 0:
            raise ValueError(f"{field.name} cannot be negative")
        return v
    

    #validators to make sure price attributes are correct
    @model_validator(mode="after")
    @classmethod
    def check_logic(cls, values):
        low = values.low
        high = values.high
        open = values.open
        close = values.close

        if not (low <= open <= high):
            raise ValueError(f"Open price {open} must be between low {low} and high {high}")
        if not (low <= close <= high):
            raise ValueError(f"Close price {close} must be between low {low} and high {high}")
        if low > high:
            raise ValueError(f"Low price {low} cannot be greater than high {high}")

        return values