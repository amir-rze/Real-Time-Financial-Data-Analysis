from sqlalchemy import  Column, Integer, String, Float, DateTime
from database import Base


# Define the Data model
class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String , index=True)
    opening_price = Column(Float)
    closing_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime)
