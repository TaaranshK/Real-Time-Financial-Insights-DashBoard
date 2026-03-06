"""
Backend API tests using pytest + FastAPI TestClient.

Run with: pytest test_apis.py -v
Uses SQLite in-memory database for testing.
"""

import pytest


def quick_auth(client):
    """Register and login a test user, return auth headers."""
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "pass1234",
    })
    resp = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "pass1234",
    })
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestAuth:
    """Auth endpoint tests."""
    
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "username": "john",
            "email": "john@mail.com",
            "password": "secret123",
        })
        assert resp.status_code == 201
        assert resp.json()["user"]["username"] == "john"
        assert "password" not in resp.json()["user"]

    def test_register_duplicate_email(self, client):
        client.post("/api/auth/register", json={
            "username": "john",
            "email": "john@mail.com",
            "password": "secret123",
        })
        resp = client.post("/api/auth/register", json={
            "username": "john2",
            "email": "john@mail.com",
            "password": "pass456",
        })
        assert resp.status_code == 400

    def test_register_invalid_email(self, client):
        resp = client.post("/api/auth/register", json={
            "username": "john",
            "email": "not-an-email",
            "password": "secret123",
        })
        assert resp.status_code == 422

    def test_register_short_password(self, client):
        resp = client.post("/api/auth/register", json={
            "username": "john",
            "email": "john@mail.com",
            "password": "abc",
        })
        assert resp.status_code == 422

    def test_login_success(self, client):
        client.post("/api/auth/register", json={
            "username": "john",
            "email": "john@mail.com",
            "password": "secret123",
        })
        resp = client.post("/api/auth/login", json={
            "email": "john@mail.com",
            "password": "secret123",
        })
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "access_token" in data
        assert data["user"]["email"] == "john@mail.com"

    def test_login_wrong_password(self, client):
        client.post("/api/auth/register", json={
            "username": "john",
            "email": "john@mail.com",
            "password": "secret123",
        })
        resp = client.post("/api/auth/login", json={
            "email": "john@mail.com",
            "password": "wrongpass",
        })
        assert resp.status_code == 401

    def test_profile_unauthorized(self, client):
        resp = client.get("/api/auth/profile")
        assert resp.status_code == 401

    def test_profile_success(self, client):
        headers = quick_auth(client)
        resp = client.get("/api/auth/profile", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["user"]["email"] == "test@example.com"

    def test_update_profile(self, client):
        headers = quick_auth(client)
        resp = client.put("/api/auth/profile", headers=headers, json={
            "first_name": "Test",
            "last_name": "User",
        })
        assert resp.status_code == 200
        assert resp.json()["user"]["first_name"] == "Test"


class TestPortfolio:
    """Portfolio endpoint tests."""
    
    def test_create_portfolio(self, client):
        headers = quick_auth(client)
        resp = client.post("/api/portfolio/portfolios", headers=headers, json={
            "name": "My Portfolio",
            "description": "Test portfolio",
        })
        assert resp.status_code == 201
        assert resp.json()["portfolio"]["name"] == "My Portfolio"

    def test_list_portfolios(self, client):
        headers = quick_auth(client)
        client.post("/api/portfolio/portfolios", headers=headers, json={"name": "P1"})
        client.post("/api/portfolio/portfolios", headers=headers, json={"name": "P2"})
        resp = client.get("/api/portfolio/portfolios", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["total"] == 2

    def test_get_portfolio_not_found(self, client):
        headers = quick_auth(client)
        resp = client.get("/api/portfolio/portfolios/999", headers=headers)
        assert resp.status_code == 404

    def test_add_holding(self, client):
        headers = quick_auth(client)
        p = client.post("/api/portfolio/portfolios", headers=headers, json={"name": "P1"})
        pid = p.json()["portfolio"]["id"]
        resp = client.post(f"/api/portfolio/portfolios/{pid}/holdings", headers=headers, json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc",
            "quantity": 10,
            "buy_price": 150.0,
        })
        assert resp.status_code == 201
        assert resp.json()["holding"]["stock_symbol"] == "AAPL"

    def test_add_holding_invalid_qty(self, client):
        headers = quick_auth(client)
        p = client.post("/api/portfolio/portfolios", headers=headers, json={"name": "P1"})
        pid = p.json()["portfolio"]["id"]
        resp = client.post(f"/api/portfolio/portfolios/{pid}/holdings", headers=headers, json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple",
            "quantity": -5,
            "buy_price": 150.0,
        })
        assert resp.status_code == 422

    def test_update_price(self, client):
        headers = quick_auth(client)
        p = client.post("/api/portfolio/portfolios", headers=headers, json={"name": "P1"})
        pid = p.json()["portfolio"]["id"]
        h = client.post(f"/api/portfolio/portfolios/{pid}/holdings", headers=headers, json={
            "stock_symbol": "TSLA",
            "stock_name": "Tesla",
            "quantity": 5,
            "buy_price": 200.0,
        })
        hid = h.json()["holding"]["id"]
        resp = client.put(f"/api/portfolio/holdings/{hid}/price", headers=headers, json={
            "new_price": 250.0,
        })
        assert resp.status_code == 200
        assert resp.json()["holding"]["current_price"] == 250.0

    def test_portfolio_summary(self, client):
        headers = quick_auth(client)
        p = client.post("/api/portfolio/portfolios", headers=headers, json={"name": "P1"})
        pid = p.json()["portfolio"]["id"]
        client.post(f"/api/portfolio/portfolios/{pid}/holdings", headers=headers, json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple",
            "quantity": 10,
            "buy_price": 100.0,
        })
        resp = client.get("/api/portfolio/summary", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["total_invested"] == 1000.0


class TestMarketAnalysis:
    """Market analysis endpoint tests."""
    
    def test_analyze_stock(self, client):
        headers = quick_auth(client)
        resp = client.post("/api/market-analysis/analyze", headers=headers, json={
            "stock_symbol": "AAPL",
        })
        assert resp.status_code == 200
        analysis = resp.json()["analysis"]
        assert analysis["stock_symbol"] == "AAPL"
        assert "summary" in analysis
        assert "market_sentiment" in analysis
        assert "recommendation" in analysis

    def test_analyze_stock_invalid(self, client):
        headers = quick_auth(client)
        resp = client.post("/api/market-analysis/analyze", headers=headers, json={
            "stock_symbol": "",
        })
        assert resp.status_code == 422

    def test_list_analyses(self, client):
        headers = quick_auth(client)
        client.post("/api/market-analysis/analyze", headers=headers, json={"stock_symbol": "AAPL"})
        client.post("/api/market-analysis/analyze", headers=headers, json={"stock_symbol": "TSLA"})
        resp = client.get("/api/market-analysis/analyses", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["total"] == 2

    def test_get_news(self, client):
        headers = quick_auth(client)
        resp = client.get("/api/market-analysis/news", headers=headers)
        assert resp.status_code == 200
        news = resp.json()["news"]
        assert len(news) > 0
        assert "title" in news[0]

    def test_ai_output_format(self, client):
        """Verify the AI analysis output has the expected structure."""
        headers = quick_auth(client)
        resp = client.post("/api/market-analysis/analyze", headers=headers, json={
            "stock_symbol": "GOOGL",
            "stock_name": "Alphabet",
            "sector": "Technology",
        })
        analysis = resp.json()["analysis"]
        rec = analysis["recommendation"]
        assert "action" in rec
        assert rec["action"] in ["BUY", "SELL", "HOLD"]
        assert "confidence" in rec
        assert rec["confidence"] in ["High", "Medium", "Low"]
        assert "reason" in rec
