from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#instrment table creation
class InstrumentDB(Base):
    __tablename__ = "Instrument_Table"

    ticker = Column(String, primary_key=True)
    company_name = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    country = Column(String, nullable=False)
    instrument_type = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)