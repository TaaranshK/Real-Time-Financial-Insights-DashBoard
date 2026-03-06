"""
Portfolio service using SQLAlchemy ORM.

Handles portfolio and holding operations.
"""

from sqlalchemy.orm import Session
from app.models.portfolio_model import Portfolio
from app.models.holding import Holding


def create_portfolio(user_id: int, name: str, description: str = None, portfolio_type: str = "Equity", db: Session = None):
    """Create a new portfolio for the user."""
    if not db:
        raise ValueError("Database session required")
    
    portfolio = Portfolio(
        user_id=user_id,
        name=name,
        description=description,
        portfolio_type=portfolio_type
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def get_user_portfolios(user_id: int, db: Session = None):
    """Get all portfolios for a user."""
    if not db:
        raise ValueError("Database session required")
    
    return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()


def get_portfolio(portfolio_id: int, user_id: int, db: Session = None):
    """Get a specific portfolio, checking ownership."""
    if not db:
        raise ValueError("Database session required")
    
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user_id
    ).first()
    return portfolio


def add_holding(portfolio_id: int, user_id: int, stock_symbol: str, stock_name: str, 
               quantity: float, buy_price: float, sector: str = None, db: Session = None):
    """Add a stock holding to a portfolio."""
    if not db:
        raise ValueError("Database session required")
    
    portfolio = get_portfolio(portfolio_id, user_id, db)
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    holding = Holding(
        portfolio_id=portfolio_id,
        stock_symbol=stock_symbol.upper(),
        stock_name=stock_name,
        quantity=quantity,
        buy_price=buy_price,
        current_price=buy_price,
        sector=sector
    )
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return holding


def get_holdings(portfolio_id: int, user_id: int, db: Session = None):
    """Get all holdings in a portfolio."""
    if not db:
        raise ValueError("Database session required")
    
    portfolio = get_portfolio(portfolio_id, user_id, db)
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    return portfolio.holdings


def update_holding_price(holding_id: int, user_id: int, new_price: float, db: Session = None):
    """Update the current price of a holding."""
    if not db:
        raise ValueError("Database session required")
    
    holding = db.query(Holding).join(Portfolio).filter(
        Holding.id == holding_id,
        Portfolio.user_id == user_id
    ).first()
    
    if not holding:
        raise ValueError("Holding not found")
    
    holding.current_price = new_price
    db.commit()
    db.refresh(holding)
    return holding


def get_portfolio_summary(user_id: int, db: Session = None):
    """Calculate portfolio statistics for the dashboard."""
    if not db:
        raise ValueError("Database session required")
    
    user_portfolios = get_user_portfolios(user_id, db)

    total_invested = 0.0
    total_current = 0.0
    total_holdings = 0

    for portfolio in user_portfolios:
        for holding in portfolio.holdings:
            total_invested += holding.buy_price * holding.quantity
            total_current += holding.current_price * holding.quantity
            total_holdings += 1

    profit_loss = total_current - total_invested
    pct_change = (profit_loss / total_invested * 100) if total_invested > 0 else 0.0

    return {
        "total_portfolios": len(user_portfolios),
        "total_holdings": total_holdings,
        "total_invested": round(total_invested, 2),
        "total_current_value": round(total_current, 2),
        "profit_loss": round(profit_loss, 2),
        "pct_change": round(pct_change, 2),
    }


