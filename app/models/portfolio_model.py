"""
Portfolio database model.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    portfolio_type = Column(String(50), default="Equity")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "portfolio_type": self.portfolio_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "holdings": [h.to_dict() for h in self.holdings] if self.holdings else [],
        }
