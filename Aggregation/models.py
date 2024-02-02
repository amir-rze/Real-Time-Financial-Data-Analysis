from sqlalchemy import Column, Integer, String, Float, DateTime


from database import Base

# Define the Data model
class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String , index=True)
    sell_count = Column(Integer)
    buy_count = Column(Integer)
