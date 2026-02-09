""" create and check price alerts"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.alert_model import Alert
from ..models.market_model import MarketPrice
from ..schemas.alert_schema import AlertCreate, AlertResponse
from ..auth.auth_validate import auth_validate
from ..services.alert_service import check_alert


router = APIRouter(prefix="/alerts", tags=["Alerts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    current_user=Depends(auth_validate),
    db: Session = Depends(get_db)
):
    """create a new price alert for the logged-in user"""
    new_alert = Alert(
        user_id=current_user["user_id"],
        asset_name=alert.asset_name,
        target_price=alert.target_price,
        condition=alert.condition
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert


@router.get("/check")
def check_my_alerts(
    current_user=Depends(auth_validate),
    db: Session = Depends(get_db)
):
    """check if any alerts are triggered based on current prices"""
    user_id = current_user["user_id"]
    alerts = db.query(Alert).filter(Alert.user_id == user_id).all()

    triggered_alerts = []

    for alert in alerts:
        latest_price = (
            db.query(MarketPrice)
            .filter(MarketPrice.asset_name == alert.asset_name)
            .order_by(MarketPrice.timestamp.desc())
            .first()
        )

        if not latest_price:
            continue

        if check_alert(alert, latest_price.price):
            message = (
                f"{alert.asset_name} price is {latest_price.price}, "
                f"alert condition met ({alert.condition} {alert.target_price})"
            )
            triggered_alerts.append(message)

    return {"alerts": triggered_alerts}

