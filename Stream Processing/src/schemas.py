from pydantic import BaseModel

# Define the Pydantic model for the Data validation
class Metrics(BaseModel):
    stock_symbol: str
    moving_avg: float
    exp_moving_avg: float
    rsi: float
    current_price:float
    