"""

What this file does:
- Add asset to portfolio: POST /portfolio/add
- Get my portfolio: GET /portfolio/me


"""


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.portfolio_model import Portfolio
from ..schemas.portfolio_schema import PortfolioCreate, PortfolioResponse
from ..auth.auth_validate import auth_validate



router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)



def get_db():
    """
    Creates a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/add", response_model=PortfolioResponse)
def add_to_portfolio(
    data: PortfolioCreate,
    current_user=Depends(auth_validate),
    db: Session = Depends(get_db)
):

    
    # Step 1: Get user id from JWT token
    user_id = current_user["user_id"]

    # Step 2: Check if user already has this asset
    existing_asset = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id)
        .filter(Portfolio.asset_name == data.asset_name)
        .first()
    )

    # Step 3: If asset exists, add to existing quantity
    if existing_asset is not None:
        existing_asset.quantity = existing_asset.quantity + data.quantity
        db.commit()
        db.refresh(existing_asset)
        return existing_asset

    # Step 4: If new asset, create new entry
    new_asset = Portfolio(
        user_id=user_id,
        asset_name=data.asset_name,
        quantity=data.quantity
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


#  GET MY PORTFOLIO 
@router.get("/me", response_model=list[PortfolioResponse])
def get_my_portfolio(
    current_user=Depends(auth_validate),
    db: Session = Depends(get_db)
):
    
    
    # Step 1: Get user id from JWT token
    user_id = current_user["user_id"]

    # Step 2: Get all portfolio items for this user
    portfolio_items = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id)
        .all()
    )

    # Step 3: Return the list
    return portfolio_items
