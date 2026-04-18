"""
Portfolio routes - manage user portfolios and holdings
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.auth_routes import get_default_user
from app.database import get_db
from app.models.schemas import HoldingRequest, PortfolioRequest, PriceUpdateRequest
from app.services.portfolio_service import (
    add_holding,
    create_portfolio,
    get_holdings,
    get_portfolio,
    get_portfolio_summary,
    get_user_portfolios,
    update_holding_price,
)

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


@router.post("/portfolios", status_code=status.HTTP_201_CREATED)
def create_portfolio_route(payload: PortfolioRequest, user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Create a new portfolio."""
    try:
        portfolio = create_portfolio(user.id, payload.name, payload.description, payload.portfolio_type, db)
        return {"message": "Portfolio created", "portfolio": portfolio.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/portfolios")
def list_portfolios(user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Get all portfolios for the user."""
    portfolios = get_user_portfolios(user.id, db)
    return {
        "message": "Portfolios retrieved",
        "portfolios": [p.to_dict() for p in portfolios],
        "total": len(portfolios)
    }


@router.get("/portfolios/{portfolio_id}")
def get_portfolio_route(portfolio_id: int, user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Get a specific portfolio."""
    portfolio = get_portfolio(portfolio_id, user.id, db)
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return {"message": "Portfolio retrieved", "portfolio": portfolio.to_dict()}


@router.post("/portfolios/{portfolio_id}/holdings", status_code=status.HTTP_201_CREATED)
def add_holding_route(portfolio_id: int, payload: HoldingRequest, user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Add a holding to a portfolio."""
    try:
        holding = add_holding(
            portfolio_id,
            user.id,
            payload.stock_symbol,
            payload.stock_name,
            payload.quantity,
            payload.buy_price,
            payload.sector,
            db
        )
        return {"message": "Holding added", "holding": holding.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/portfolios/{portfolio_id}/holdings")
def get_holdings_route(portfolio_id: int, user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Get all holdings in a portfolio."""
    try:
        holdings = get_holdings(portfolio_id, user.id, db)
        return {
            "message": "Holdings retrieved",
            "holdings": [h.to_dict() for h in holdings],
            "total": len(holdings)
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/holdings/{holding_id}/price")
def update_price_route(holding_id: int, payload: PriceUpdateRequest, user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Update the price of a holding."""
    try:
        holding = update_holding_price(holding_id, user.id, payload.new_price, db)
        return {"message": "Price updated", "holding": holding.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/summary")
def portfolio_summary_route(user=Depends(get_default_user), db: Session = Depends(get_db)):
    """Get portfolio summary statistics."""
    return get_portfolio_summary(user.id, db)
