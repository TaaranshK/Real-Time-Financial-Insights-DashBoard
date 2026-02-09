"""

What this file does:
- MarketInput: what we need when adding a new price
- MarketOutput: what we send back when returning prices

Example:
- Someone adds: {"asset_name": "BTC", "price": 42000}
- We return: {"id": 1, "asset_name": "BTC", "price": 42000, "timestamp": "..."}
"""


from pydantic import BaseModel
from datetime import datetime



class MarketInput(BaseModel):
   
    
    # Which asset (BTC, ETH, AAPL, etc.)
    asset_name: str
    
    # The price value
    price: float


class MarketOutput(BaseModel):
    """
    What data we send back when returning market prices.
    """
    
    # Unique ID from database
    id: int
    
    # Which asset
    asset_name: str
    
    # The price value
    price: float
    
    # When this price was recorded
    timestamp: datetime

    # This tells Pydantic to read data from SQLAlchemy model
    class Config:
        from_attributes = True
