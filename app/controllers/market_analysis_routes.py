"""
Market analysis routes - AI-powered stock analysis and news
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.auth_routes import get_default_user
from app.database import get_db
from app.models.schemas import AnalyzeRequest
from app.services.market_analysis_service import analyze_stock, get_news, get_user_analyses

router = APIRouter(prefix="/api/market-analysis", tags=["analysis"])


@router.post("/analyze")
def analyze_stock_route(payload: AnalyzeRequest, user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Run AI analysis on a stock."""
    try:
        analysis = analyze_stock(
            user.id,
            payload.stock_symbol,
            payload.stock_name,
            payload.current_price,
            payload.sector,
            db
        )
        return {"message": "Analysis completed", "analysis": analysis.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/analyses")
def list_analyses(limit: int = 10, user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Get past analyses for the user."""
    records = get_user_analyses(user.id, limit, db)
    return {
        "message": "Analyses retrieved",
        "analyses": [r.to_dict() for r in records],
        "total": len(records)
    }


@router.get("/news")
def get_market_news():
    """Get latest market news."""
    news = get_news()
    return {"message": "News retrieved", "news": news}
