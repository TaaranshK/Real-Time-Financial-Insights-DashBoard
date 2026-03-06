"""
Market Analysis database model (AI-generated stock analysis).
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.database import Base


class MarketAnalysis(Base):
    __tablename__ = "market_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_symbol = Column(String(10), nullable=False)
    summary = Column(String(1000), nullable=True)
    market_sentiment = Column(String(50), default="Neutral")
    recommendation = Column(JSON, nullable=True)
    news_headlines = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "stock_symbol": self.stock_symbol,
            "summary": self.summary,
            "market_sentiment": self.market_sentiment,
            "recommendation": self.recommendation,
            "news_headlines": self.news_headlines,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
