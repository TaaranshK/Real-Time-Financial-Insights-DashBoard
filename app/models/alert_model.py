from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Which user owns this alert
    user_id = Column(Integer, ForeignKey("users.id"))

    # Asset name (BTC, ETH, etc.)
    asset_name = Column(String, nullable=False)

    # Price 
    target_price = Column(Float, nullable=False)

    # Condition: above / below
    condition = Column(String, nullable=False)
