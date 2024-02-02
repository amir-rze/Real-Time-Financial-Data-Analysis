from pydantic import BaseModel

# Define the Pydantic model for the Data validation
class SummaryOut(BaseModel):
    stock_symbol: str
    sell_count: int
    buy_count: int
