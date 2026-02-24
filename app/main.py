from datetime import datetime
from typing import Any
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Financial Monitoring System API")

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


# In-memory stores so the project runs cleanly without database migration work.
USERS: dict[str, dict[str, Any]] = {}
TOKENS: dict[str, str] = {}
PORTFOLIOS: dict[int, dict[str, Any]] = {}
ANALYSES: dict[int, dict[str, Any]] = {}
NEXT_IDS = {"portfolio": 1, "holding": 1, "analysis": 1}


def _next_id(key: str) -> int:
    value = NEXT_IDS[key]
    NEXT_IDS[key] += 1
    return value


def _bearer_token(auth_header: str | None) -> str | None:
    if not auth_header:
        return None
    parts = auth_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip()


def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    token = _bearer_token(authorization)
    user_id = TOKENS.get(token or "")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return USERS[user_id]


class RegisterIn(BaseModel):
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class LoginIn(BaseModel):
    email: str
    password: str


class PortfolioIn(BaseModel):
    name: str
    description: str | None = None
    portfolio_type: str = "Equity"


class HoldingIn(BaseModel):
    stock_symbol: str
    stock_name: str
    quantity: float
    buy_price: float
    sector: str | None = None


class PriceUpdateIn(BaseModel):
    new_price: float


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Financial Monitoring API", "docs": "/docs"}


@app.post("/api/auth/register")
def register(payload: RegisterIn) -> dict[str, Any]:
    if any(u["email"].lower() == payload.email.lower() for u in USERS.values()):
        raise HTTPException(status_code=400, detail="Email already exists")
    user_id = str(uuid4())
    USERS[user_id] = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "password": payload.password,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "phone": payload.phone,
        "role": "USER",
        "created_at": datetime.utcnow().isoformat(),
    }
    user_view = {k: v for k, v in USERS[user_id].items() if k != "password"}
    return {"message": "User registered successfully", "user": user_view}


@app.post("/api/auth/login")
def login(payload: LoginIn) -> dict[str, Any]:
    user = next((u for u in USERS.values() if u["email"].lower() == payload.email.lower()), None)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = str(uuid4())
    refresh_token = str(uuid4())
    TOKENS[access_token] = user["id"]
    user_view = {k: v for k, v in user.items() if k != "password"}
    return {
        "message": "Login successful",
        "data": {"access_token": access_token, "refresh_token": refresh_token, "user": user_view},
    }


@app.get("/api/auth/profile")
def get_profile(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    user_view = {k: v for k, v in user.items() if k != "password"}
    return {"message": "Profile retrieved successfully", "user": user_view}


@app.put("/api/auth/profile")
def update_profile(payload: dict[str, Any], user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    for field in ("first_name", "last_name", "phone", "username"):
        if field in payload:
            user[field] = payload[field]
    user_view = {k: v for k, v in user.items() if k != "password"}
    return {"message": "Profile updated successfully", "user": user_view}


@app.post("/api/auth/refresh-token")
def refresh_token(_: dict[str, str]) -> dict[str, str]:
    return {"message": "Token refreshed successfully", "access_token": str(uuid4())}


@app.post("/api/portfolio/portfolios")
def create_portfolio(payload: PortfolioIn, user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    portfolio_id = _next_id("portfolio")
    data = {
        "id": portfolio_id,
        "user_id": user["id"],
        "name": payload.name,
        "description": payload.description,
        "portfolio_type": payload.portfolio_type,
        "holdings": [],
        "created_at": datetime.utcnow().isoformat(),
    }
    PORTFOLIOS[portfolio_id] = data
    return {"message": "Portfolio created successfully", "portfolio": data}


@app.get("/api/portfolio/portfolios")
def list_portfolios(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    portfolios = [p for p in PORTFOLIOS.values() if p["user_id"] == user["id"]]
    return {"message": "Portfolios retrieved successfully", "portfolios": portfolios, "total": len(portfolios)}


@app.get("/api/portfolio/portfolios/{portfolio_id}")
def get_portfolio(portfolio_id: int, user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    portfolio = PORTFOLIOS.get(portfolio_id)
    if not portfolio or portfolio["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return {"message": "Portfolio retrieved successfully", "portfolio": portfolio}


@app.post("/api/portfolio/portfolios/{portfolio_id}/holdings")
def add_holding(portfolio_id: int, payload: HoldingIn, user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    portfolio = PORTFOLIOS.get(portfolio_id)
    if not portfolio or portfolio["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    holding = {
        "id": _next_id("holding"),
        "stock_symbol": payload.stock_symbol.upper(),
        "stock_name": payload.stock_name,
        "quantity": payload.quantity,
        "buy_price": payload.buy_price,
        "sector": payload.sector,
        "current_price": payload.buy_price,
    }
    portfolio["holdings"].append(holding)
    return {"message": "Holding added successfully", "holding": holding}


@app.get("/api/portfolio/portfolios/{portfolio_id}/holdings")
def get_holdings(portfolio_id: int, user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    portfolio = PORTFOLIOS.get(portfolio_id)
    if not portfolio or portfolio["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    holdings = portfolio["holdings"]
    return {"message": "Holdings retrieved successfully", "holdings": holdings, "total": len(holdings)}


@app.put("/api/portfolio/holdings/{holding_id}/price")
def update_price(holding_id: int, payload: PriceUpdateIn, user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    for portfolio in PORTFOLIOS.values():
        if portfolio["user_id"] != user["id"]:
            continue
        for holding in portfolio["holdings"]:
            if holding["id"] == holding_id:
                holding["current_price"] = payload.new_price
                return {"message": "Holding price updated", "holding": holding}
    raise HTTPException(status_code=404, detail="Holding not found")


@app.post("/api/market-analysis/analyze")
def analyze_stock(payload: dict[str, Any], user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    symbol = str(payload.get("stock_symbol", "")).upper().strip()
    if not symbol:
        raise HTTPException(status_code=400, detail="stock_symbol is required")
    analysis_id = _next_id("analysis")
    result = {
        "id": analysis_id,
        "user_id": user["id"],
        "stock_symbol": symbol,
        "sentiment": "NEUTRAL",
        "recommendation": "HOLD",
        "created_at": datetime.utcnow().isoformat(),
    }
    ANALYSES[analysis_id] = result
    return {"message": "Analysis completed successfully", "analysis": result}


@app.get("/api/market-analysis/analyses")
def list_analyses(limit: int = 10, user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    records = [a for a in ANALYSES.values() if a["user_id"] == user["id"]][:limit]
    return {"message": "Analyses retrieved successfully", "analyses": records, "total": len(records)}
