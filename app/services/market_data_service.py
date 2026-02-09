"""


What this file does:
- Runs in background when server starts
- Generates fake BTC prices every 5 seconds
- Saves them to database

"""

import time
import random
from sqlalchemy.orm import Session

from ..models.market_model import MarketPrice



def generate_fake_price(asset_name):
  
    return random.uniform(40000, 45000)


#Save The Price To the Database
def save_price_to_db(db: Session, asset_name: str):
    """
    Creates a price entry and saves to database.
    """
    
    # Step 1: Generate a price
    price = generate_fake_price(asset_name)

    # Step 2: Create price object
    new_price = MarketPrice(
        asset_name=asset_name,
        price=price
    )

    # Step 3: Save to database
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    
    print(f"Saved price: {asset_name} = ${price:.2f}")


def start_price_generator(db: Session):
    """
    Runs forever, saving a BTC price every 5 seconds.
    This is called when server starts.
    """
    
    print("Price generator started!")
    
    while True:
        # Save a BTC price
        save_price_to_db(db, "BTC")

        # Wait 5 seconds
        time.sleep(5)
