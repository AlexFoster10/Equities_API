from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.logger import get_logger
import models.instrumentDB as InstrumentDB
import models.priceDB as PriceDB
logger = get_logger()

DB_FILE = "sqlite:///app/data/equities.db"

engine = create_engine(DB_FILE, connect_args={"check_same_thread": False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
    

def create_instrument_table():
    InstrumentDB.Base.metadata.create_all(bind=engine)

def create_prices_table():
    PriceDB.Base.metadata.create_all(bind=engine)


##create generic search function
def search_instrument_by_symbol(db, InstrumentDB, PriceDB):
    print("")








     
    

    
        

