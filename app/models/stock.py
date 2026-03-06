"""
Stock database model.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from app.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=True)
    current_price = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "name": self.name,
            "sector": self.sector,
            "current_price": self.current_price,
            "market_cap": self.market_cap,
            "pe_ratio": self.pe_ratio,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
