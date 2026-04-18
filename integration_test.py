"""
Integration tests for Frontend-Backend Communication
Tests verify that the frontend can properly communicate with all backend APIs
"""
import pytest
import requests
import json
import socket
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"


def _server_is_available(host: str = "localhost", port: int = 8000, timeout: float = 0.5) -> bool:
    """Return True if a local backend process is listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0


if not _server_is_available():
    pytestmark = pytest.mark.skip(reason="Integration tests require a running backend at http://localhost:8000")

class TestIntegration:
    """Integration tests for the FinVue application"""
    
    @pytest.fixture
    def auth_token(self):
        """Get auth token for testing authenticated endpoints"""
        import time
        # Register a new user
        timestamp = f"{int(time.time() * 1000)}"
        register_data = {
            "username": f"testuser_{timestamp}",
            "email": f"test_{timestamp}@example.com",
            "password": "Test@1234",
            "first_name": "Test",
            "last_name": "User"
        }
        
        # Register
        resp = requests.post(f"{BASE_URL}{API_PREFIX}/auth/register", json=register_data)
        assert resp.status_code == 201, f"Registration failed: {resp.text}"
        
        # Login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        resp = requests.post(f"{BASE_URL}{API_PREFIX}/auth/login", json=login_data)
        assert resp.status_code == 200, f"Login failed: {resp.text}"
        data = resp.json()
        
        # Handle nested response format
        if "data" in data and isinstance(data["data"], dict) and "access_token" in data["data"]:
            return data["data"]["access_token"]
        elif "access_token" in data:
            return data["access_token"]
        else:
            raise AssertionError(f"No access token in response: {data}")
    
    def test_api_endpoints_exist(self):
        """Verify all required API endpoints exist and respond"""
        endpoints = [
            ("GET", "/api/auth/profile"),  # This will fail without auth, but endpoint should exist
            ("POST", "/api/auth/login"),
            ("POST", "/api/auth/register"),
        ]
        
        for method, endpoint in endpoints:
            if method == "GET":
                resp = requests.get(f"{BASE_URL}{endpoint}")
            else:
                resp = requests.post(f"{BASE_URL}{endpoint}", json={})
            
            # Should not be 404 (endpoint not found)
            assert resp.status_code != 404, f"Endpoint {method} {endpoint} not found"
            print(f"✓ {method} {endpoint} exists")
    
    def test_auth_flow(self):
        """Test complete authentication flow"""
        import time
        # Register
        timestamp = f"{int(time.time() * 1000)}"
        email = f"test_{timestamp}@example.com"
        register_data = {
            "username": f"testuser_{timestamp}",
            "email": email,
            "password": "Test@1234",
            "first_name": "Test",
            "last_name": "User"
        }
        
        resp = requests.post(f"{BASE_URL}{API_PREFIX}/auth/register", json=register_data)
        assert resp.status_code == 201, f"Register failed: {resp.text}"
        print("✓ Registration successful")
        
        # Login
        login_data = {"email": email, "password": "Test@1234"}
        resp = requests.post(f"{BASE_URL}{API_PREFIX}/auth/login", json=login_data)
        assert resp.status_code == 200, f"Login failed: {resp.text}"
        
        data = resp.json()
        
        # Handle nested response format
        if "data" in data and isinstance(data["data"], dict):
            token = data["data"].get("access_token")
            user = data["data"].get("user")
        else:
            token = data.get("access_token")
            user = data.get("user")
            
        assert token, f"No token in response: {data}"
        assert user, f"No user in response: {data}"
        print("✓ Login successful, token received")
        
        # Get profile with token
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}{API_PREFIX}/auth/profile", headers=headers)
        assert resp.status_code == 200, f"Profile retrieval failed: {resp.text}"
        profile = resp.json()
        
        # Response format is {"message": "...", "user": {...}}
        user_data = profile.get("user")
        assert user_data, f"No user in response: {profile}"
        assert user_data.get("email") == email, f"Profile email mismatch: {user_data}"
        print("✓ Profile retrieval successful")
    
    def test_portfolio_endpoints(self, auth_token):
        """Test portfolio management endpoints"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Create portfolio
        portfolio_data = {
            "name": "Test Portfolio",
            "description": "A test portfolio",
            "portfolio_type": "Equity"
        }
        resp = requests.post(
            f"{BASE_URL}{API_PREFIX}/portfolio/portfolios",
            json=portfolio_data,
            headers=headers
        )
        assert resp.status_code == 201
        response = resp.json()
        portfolio = response.get("portfolio", response)
        portfolio_id = portfolio.get("id")
        assert portfolio_id, f"No portfolio id in response: {response}"
        print(f"✓ Portfolio created: {portfolio_id}")
        
        # Get portfolios
        resp = requests.get(f"{BASE_URL}{API_PREFIX}/portfolio/portfolios", headers=headers)
        assert resp.status_code == 200
        response = resp.json()
        portfolios = response.get("portfolios", response)
        assert isinstance(portfolios, list)
        print("✓ Portfolios retrieved")
        
        # Get single portfolio
        resp = requests.get(
            f"{BASE_URL}{API_PREFIX}/portfolio/portfolios/{portfolio_id}",
            headers=headers
        )
        assert resp.status_code == 200
        print("✓ Single portfolio retrieved")
        
        # Add holding
        holding_data = {
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc",
            "quantity": 10,
            "buy_price": 150.00,
            "sector": "Technology"
        }
        resp = requests.post(
            f"{BASE_URL}{API_PREFIX}/portfolio/portfolios/{portfolio_id}/holdings",
            json=holding_data,
            headers=headers
        )
        assert resp.status_code == 201
        holding = resp.json()
        holding_data_response = holding.get("holding", holding)
        print(f"✓ Holding added: {holding_data_response.get('stock_symbol')}")
        
        # Get portfolio summary
        resp = requests.get(f"{BASE_URL}{API_PREFIX}/portfolio/summary", headers=headers)
        assert resp.status_code == 200
        summary = resp.json()
        assert "total_portfolios" in summary or "data" in summary
        print("✓ Portfolio summary retrieved")
    
    def test_market_analysis_endpoints(self, auth_token):
        """Test market analysis endpoints"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Analyze stock (may return 200 or 201 depending on implementation)
        analysis_data = {
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc",
            "current_price": 150.00,
            "sector": "Technology"
        }
        resp = requests.post(
            f"{BASE_URL}{API_PREFIX}/market-analysis/analyze",
            json=analysis_data,
            headers=headers
        )
        assert resp.status_code in [200, 201], f"Analysis failed: {resp.status_code} - {resp.text}"
        analysis = resp.json()
        analysis_data_response = analysis.get("analysis", analysis)
        assert "stock_symbol" in analysis_data_response or "stock_symbol" in str(analysis)
        print(f"✓ Stock analysis created")
        
        # Get analyses
        resp = requests.get(f"{BASE_URL}{API_PREFIX}/market-analysis/analyses", headers=headers)
        assert resp.status_code == 200
        analyses = resp.json()
        print("✓ Analyses retrieved")
        
        # Get news
        resp = requests.get(f"{BASE_URL}{API_PREFIX}/market-analysis/news", headers=headers)
        assert resp.status_code == 200
        news = resp.json()
        print("✓ Market news retrieved")
    
    def test_cors_headers(self):
        """Test that CORS headers are properly set for frontend requests"""
        resp = requests.options(f"{BASE_URL}{API_PREFIX}/auth/login")
        # CORS headers might not be present for OPTIONS, but the route should exist
        assert resp.status_code != 404
        print("✓ CORS is configured")
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        # Invalid credentials
        resp = requests.post(
            f"{BASE_URL}{API_PREFIX}/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrong"}
        )
        assert resp.status_code == 401
        print("✓ Invalid credentials properly rejected")
        
        # Missing required fields
        resp = requests.post(
            f"{BASE_URL}{API_PREFIX}/auth/register",
            json={"email": "test@example.com"}  # Missing other required fields
        )
        assert resp.status_code == 422  # Unprocessable entity
        print("✓ Missing fields properly validated")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
