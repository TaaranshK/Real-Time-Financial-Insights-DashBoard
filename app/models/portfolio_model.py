"""


What this file does:
- Defines the "portfolio" table structure
- Stores which user owns which assets and how much

"""


from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base


class Portfolio(Base):
    
    # Name of the table in database
    __tablename__ = "portfolio"

    # Column 1: id - unique number for each entry
    id = Column(Integer, primary_key=True, index=True)

    # Column 2: user_id - which user owns this asset
    # ForeignKey links this to the "users" table
    user_id = Column(Integer, ForeignKey("users.id"))

    # Column 3: asset_name - name of the asset (BTC, ETH, etc.)
    asset_name = Column(String, index=True)

    # Column 4: quantity - how much of this asset the user owns
    quantity = Column(Float)
