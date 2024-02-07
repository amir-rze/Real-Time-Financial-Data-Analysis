from pydantic import BaseModel
from datetime import datetime,timedelta

# Define the Pydantic model for the Data validation
class DataIn(BaseModel):
    stock_symbol: str
    opening_price: float
    closing_price: float
    high: float
    low: float
    volume: int
    timestamp: datetime

class AdditionalDataInOrder(BaseModel):
    data_type:str
    timestamp:datetime
    stock_symbol:str
    order_type:str
    price:float
    quantity:float

class AdditionalDataInNews(BaseModel):
    data_type:str
    timestamp:datetime
    stock_symbol:str
    sentiment_score:float
    sentiment_magnitude:float
    
class AdditionalDataInMarket(BaseModel):
    data_type:str
    timestamp:datetime
    stock_symbol:str
    market_cap: float
    pe_ratio: float

class AdditionalDataInEconomic(BaseModel):
    data_type:str
    timestamp:datetime
    indicator_name: str
    value: float

# Define the Pydantic model for the Data response validation
class DataOut(BaseModel):
    stock_symbol: str
    opening_price: float
    closing_price: float
    high: float
    low: float
    volume: int
    timestamp: datetime

