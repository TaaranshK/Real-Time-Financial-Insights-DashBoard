"""
portfolio_schema.py - Defines how Portfolio data looks in API
=============================================================

What this file does:
- PortfolioCreate: what we need when adding asset to portfolio
- PortfolioResponse: what we send back when returning portfolio

Example:
- User adds: {"asset_name": "BTC", "quantity": 0.5}
- We return: {"id": 1, "user_id": 1, "asset_name": "BTC", "quantity": 0.5}
"""


from pydantic import BaseModel



class PortfolioCreate(BaseModel):
  
    
    # Which asset to add (BTC, ETH, etc.)
    asset_name: str
    
    # How much of this asset to add
    quantity: float



class PortfolioResponse(BaseModel):
    
    
    # Unique ID from database
    id: int
    
    # Which user owns this
    user_id: int
    
    # Which asset
    asset_name: str
    
    # How much they own
    quantity: float

   
    class Config:
        from_attributes = True
