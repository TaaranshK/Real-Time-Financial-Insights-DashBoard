"""
market_controller.py - Handles Market Price APIs
=================================================

What this file does:
- Add a price: POST /market/price
- Get latest prices: GET /market/latest/{asset_name}
- Get prices by time range: GET /market/history/{asset_name}

These are the APIs for managing market prices.
"""

#  IMPORTS
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..database import SessionLocal
from ..models.market_model import MarketPrice
from ..schemas.market_schema import MarketInput, MarketOutput


#  CREATE ROUTER 
# All routes in this file will start with /market
router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


#  DATABASE SESSION 
def get_db():
    """
    Creates a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  ADD MARKET PRICE 
@router.post("/price", response_model=MarketOutput)
def add_market_price(data: MarketInput, db: Session = Depends(get_db)):
    
    
    # Step 1: Create new price object
    new_price = MarketPrice(
        asset_name=data.asset_name,
        price=data.price
    )
    
    # Step 2: Save to database
    db.add(new_price)
    db.commit()
    db.refresh(new_price)

    return new_price


#  GET LATEST PRICES 
@router.get("/latest/{asset_name}", response_model=list[MarketOutput])
def get_latest_prices(asset_name: str, db: Session = Depends(get_db)):
    """
    Get the latest 10 prices for an asset.
    
    URL: GET /market/latest/BTC
    Returns: list of recent prices (newest first)
    """
    
    # Query database for this asset's prices
    # Order by timestamp descending (newest first)
    # Limit to 10 results
    prices = (
        db.query(MarketPrice)
        .filter(MarketPrice.asset_name == asset_name)
        .order_by(MarketPrice.timestamp.desc())
        .limit(10)
        .all()
    )
    
    return prices


#  GET PRICES BY TIME RANGE 
@router.get("/history/{asset_name}", response_model=list[MarketOutput])
def get_price_history(
    asset_name: str,
    hours: int = Query(default=24, description="How many hours of data to get"),
    db: Session = Depends(get_db)
):
    """
    Get price history for a time range.
    Uses composite index (asset_name, timestamp) for fast queries.
    
    URL: GET /market/history/BTC?hours=24
    Returns: list of prices from last N hours
    """
    
    # Calculate the start time
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Query with time range filter (uses idx_asset_timestamp index)
    prices = (
        db.query(MarketPrice)
        .filter(MarketPrice.asset_name == asset_name)
        .filter(MarketPrice.timestamp >= start_time)
        .order_by(MarketPrice.timestamp.asc())
        .all()
    )
    
    return prices
