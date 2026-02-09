"""

What this file does:
- Defines the "market_prices" table structure
- Stores price history for assets like BTC, ETH, etc.
- Optimized for time-series queries with proper indexes

"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from datetime import datetime
from .base import Base



class MarketPrice(Base):
    
    # Name of the table in database
    __tablename__ = "market_prices"

    # Column 1: id - unique number for each price entry
    id = Column(Integer, primary_key=True, index=True)

    # Column 2: asset_name - which asset (BTC, ETH, AAPL, etc.)
    asset_name = Column(String, index=True)
    
    # Column 3: price - the actual price value
    price = Column(Float)

    # Column 4: timestamp - when was this price recorded (indexed for fast time queries)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Composite index for efficient time-range queries per asset
    # Example: "Get BTC prices from last 24 hours" uses this index
    __table_args__ = (
        Index('idx_asset_timestamp', 'asset_name', 'timestamp'),
    )
