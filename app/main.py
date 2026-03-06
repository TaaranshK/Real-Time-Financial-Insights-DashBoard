"""
Financial Monitoring System API

Main app setup and route includes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import models for SQLAlchemy table creation (needed for create_all)
from app.models import user, portfolio_model, holding, stock, market_analysis
from app.controllers import auth_routes, portfolio_routes, market_analysis_routes

app = FastAPI(title="Financial Monitoring System API")

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(auth_routes.router)
app.include_router(portfolio_routes.router)
app.include_router(market_analysis_routes.router)


@app.get("/")
def home():
    return {"message": "Financial Monitoring API", "docs": "/docs"}
