"""
Holding database model (stocks held in a portfolio).
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    stock_symbol = Column(String(10), nullable=False)
    stock_name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=False)
    current_price = Column(Float, default=0.0)
    sector = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    portfolio = relationship("Portfolio", back_populates="holdings")

    def to_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "stock_symbol": self.stock_symbol,
            "stock_name": self.stock_name,
            "quantity": self.quantity,
            "buy_price": self.buy_price,
            "current_price": self.current_price,
            "sector": self.sector,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
