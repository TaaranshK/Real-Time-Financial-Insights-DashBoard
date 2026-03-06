"""
Market analysis service using SQLAlchemy ORM.

Handles stock analysis orchestration and news retrieval.
"""

from sqlalchemy.orm import Session
from app.models.market_analysis import MarketAnalysis
from app.services.ai_service import analyze_stock_with_ai, get_mock_news


def analyze_stock(user_id: int, stock_symbol: str, stock_name: str = None, current_price: float = None, sector: str = None, db: Session = None):
    """Run AI analysis on a stock and save the result."""
    if not db:
        raise ValueError("Database session required")
    
    symbol = stock_symbol.upper().strip()
    if not symbol:
        raise ValueError("stock_symbol is required")

    ai_result = analyze_stock_with_ai(symbol, {
        "name": stock_name or symbol,
        "current_price": current_price,
        "sector": sector,
    })

    analysis = MarketAnalysis(
        user_id=user_id,
        stock_symbol=symbol,
        summary=ai_result.get("summary", ""),
        market_sentiment=ai_result.get("market_sentiment", "Neutral"),
        recommendation=ai_result.get("recommendation", {}),
        news_headlines=ai_result.get("news_headlines", [])
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_user_analyses(user_id: int, limit: int = 10, db: Session = None):
    """Get past analyses for a user, newest first."""
    if not db:
        raise ValueError("Database session required")
    
    records = db.query(MarketAnalysis).filter(
        MarketAnalysis.user_id == user_id
    ).order_by(MarketAnalysis.created_at.desc()).limit(limit).all()
    return records


def get_news():
    """Get market news."""
    return get_mock_news()
