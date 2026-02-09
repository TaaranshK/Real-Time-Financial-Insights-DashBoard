"""
main.py - starts the FastAPI server
run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread

from .database import engine, SessionLocal
from .models.base import Base
from .models.user_model import User
from .models.market_model import MarketPrice
from .models.portfolio_model import Portfolio
from .models.alert_model import Alert
from .services.market_data_service import start_price_generator

from .controllers.ai_controller import router as ai_router
from .controllers.alert_controller import router as alert_router
from .controllers.auth_controller import router as auth_router
from .controllers.market_controller import router as market_router
from .controllers.portfolio_controller import router as portfolio_router
from .controllers.user_controller import router as user_router
from .controllers.ws_market_controller import router as ws_router


# create app
app = FastAPI(title="Financial Monitoring System")

# allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Financial Monitoring API", "docs": "/docs"}


# register all routes
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(portfolio_router)
app.include_router(market_router)
app.include_router(ai_router)
app.include_router(alert_router)
app.include_router(ws_router)


@app.on_event("startup")
def on_startup():
    """start background price generator when server starts"""
    db = SessionLocal()
    thread = Thread(target=start_price_generator, args=(db,), daemon=True)
    thread.start()
    print("Server started! Price generator running.")