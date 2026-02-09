"""test_apis.py - tests all backend APIs"""
import requests
import json

BASE = "http://localhost:8000"

def test_login():
    print("\n=== Testing Login ===")
    r = requests.post(f"{BASE}/auth/login", json={"email": "test@example.com"})
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Token received: {data.get('access_token', 'NO TOKEN')[:50]}...")
    return data.get('access_token')

def test_market_latest():
    print("\n=== Testing Market Latest ===")
    r = requests.get(f"{BASE}/market/latest/BTC")
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Got {len(data)} prices")
    if data:
        print(f"Latest: ${data[0]['price']:.2f}")

def test_market_history():
    print("\n=== Testing Market History ===")
    r = requests.get(f"{BASE}/market/history/BTC?hours=1")
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Got {len(data)} prices from last hour")

def test_ai_summary():
    print("\n=== Testing AI Summary ===")
    r = requests.get(f"{BASE}/ai/market-summary/BTC")
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Risk: {data.get('risk')}")
    print(f"Trend: {data.get('trend')}")
    print(f"Analysis: {data.get('analysis', '')[:100]}...")

def test_user_profile(token):
    print("\n=== Testing User Profile ===")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/users/me", headers=headers)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"User: {r.json()}")
    else:
        print(f"Error: {r.text}")

def test_portfolio(token):
    print("\n=== Testing Portfolio ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Add to portfolio
    r = requests.post(f"{BASE}/portfolio/add", 
                      headers=headers,
                      json={"asset_name": "BTC", "quantity": 0.5})
    print(f"Add Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Added: {r.json()}")
    
    # Get portfolio
    r = requests.get(f"{BASE}/portfolio/me", headers=headers)
    print(f"Get Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Portfolio: {len(r.json())} items")

if __name__ == "__main__":
    print("Testing all APIs...")
    
    token = test_login()
    test_market_latest()
    test_market_history()
    test_ai_summary()
    
    if token:
        test_user_profile(token)
        test_portfolio(token)
    
    print("\n=== All tests complete! ===")
