"""


What this file does:
- Get AI market summary: GET /ai/market-summary/{asset_name}

This API uses AI to analyze market data and give insights.
"""


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.market_model import MarketPrice
from ..services.ai_service import generate_ai_response
from ..utils.risk_utils import calculate_risk
from ..utils.forecast_utils import analyze_trend


#  CREATE ROUTER 

router = APIRouter(
    prefix="/ai",
    tags=["AI Analysis"]
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


#  GET MARKET SUMMARY 
@router.get("/market-summary/{asset_name}")
def market_summary(asset_name: str, db: Session = Depends(get_db)):
   
    
    # Step 1: Get recent prices from database
    prices = (
        db.query(MarketPrice)
        .filter(MarketPrice.asset_name == asset_name)
        .order_by(MarketPrice.timestamp.desc())
        .limit(10)
        .all()
    )

    # Step 2: Calculate risk level
    risk = calculate_risk(prices)

    # Step 3: Analyze price trend
    trend = analyze_trend(prices)

    # Step 4: Get AI analysis
    ai_result = generate_ai_response(asset_name, prices, risk)

    # Step 5: Return all analysis data
    return {
        "asset": asset_name,
        "risk": risk,
        "trend": trend,
        "analysis": ai_result.get("analysis", ai_result.get("ai_answer", ""))
    }
