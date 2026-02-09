"""
ws_market_controller.py - Handles WebSocket for Real-Time Prices
================================================================

What this file does:
- Streams live market prices to connected clients
- Uses WebSocket (keeps connection open)

How WebSocket works:
- REST API: request -> response -> connection closed
- WebSocket: connection stays open -> server keeps sending data

Usage:
- Connect to ws://localhost:8000/ws/market/BTC
- Server sends price every 5 seconds
"""

# ============ IMPORTS ============
import asyncio
from fastapi import APIRouter, WebSocket
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.market_model import MarketPrice


# ============ CREATE ROUTER ============
router = APIRouter()


# ============ WEBSOCKET ENDPOINT ============
@router.websocket("/ws/market/{asset_name}")
async def market_price_stream(websocket: WebSocket, asset_name: str):
    """
    Stream live prices for an asset.
    
    URL: ws://localhost:8000/ws/market/BTC
    
    Once connected, server sends latest price every 5 seconds:
    {"asset": "BTC", "price": 42000, "time": "..."}
    """
    
    # Step 1: Accept the WebSocket connection
    await websocket.accept()
    
    # Step 2: Create database session
    db: Session = SessionLocal()

    try:
        # Step 3: Keep running forever (until client disconnects)
        while True:
            
            # Step 4: Get latest price from database
            prices = (
                db.query(MarketPrice)
                .filter(MarketPrice.asset_name == asset_name)
                .order_by(MarketPrice.timestamp.desc())
                .limit(1)
                .all()
            )
            
            # Step 5: If we have a price, send it
            if len(prices) > 0:
                latest_price = prices[0]
                
                # Send as JSON to client
                await websocket.send_json({
                    "asset": latest_price.asset_name,
                    "price": latest_price.price,
                    "time": str(latest_price.timestamp)
                })

            # Step 6: Wait 5 seconds before sending again
            await asyncio.sleep(5)

    except Exception:
        # Client disconnected - this is normal
        pass
    
    finally:
        # Step 7: Close database connection
        db.close()
