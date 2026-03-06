"""
Quick login flow test - register then login.

Run with: pytest test_login.py -v
Uses SQLite in-memory database for testing.
"""

import pytest


def test_register_and_login(client):
    """Test complete user registration and login flow."""
    # Register a new user
    reg = client.post("/api/auth/register", json={
        "username": "demo",
        "email": "demo@example.com",
        "password": "password123",
    })
    assert reg.status_code == 201

    # Login with credentials
    login = client.post("/api/auth/login", json={
        "email": "demo@example.com",
        "password": "password123",
    })
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]
    assert token is not None

    # Verify profile is accessible with token
    profile = client.get("/api/auth/profile", headers={
        "Authorization": f"Bearer {token}",
    })
    assert profile.status_code == 200
    assert profile.json()["user"]["email"] == "demo@example.com"
