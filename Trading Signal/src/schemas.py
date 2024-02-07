from pydantic import BaseModel

# Define the Pydantic model for the Data validation
class Signals(BaseModel):
    stock_symbol: str
    signal: str

    