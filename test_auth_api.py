#!/usr/bin/env python
"""Test the full auth API."""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

print("=" * 50)
print("Testing Authentication API")
print("=" * 50)

# Test registration
print("\n1. Register new user:")
r = requests.post(f'{BASE_URL}/auth/register', json={
    'username': 'testuser3',
    'email': 'test3@example.com',
    'password': 'Test123!'
})
print(f"   Status: {r.status_code}")
if r.status_code == 201:
    print(f"   Response: {r.json()}")
    user_id = r.json().get('id')
else:
    print(f"   Error: {r.text}")

# Test login
print("\n2. Login:")
r = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'test3@example.com',
    'password': 'Test123!'
})
print(f"   Status: {r.status_code}")
print(f"   Response: {json.dumps(r.json(), indent=2)}")

# Test password reset request
print("\n3. Request password reset (forgot password):")
r = requests.post(f'{BASE_URL}/auth/forgot-password', json={
    'email': 'test3@example.com'
})
print(f"   Status: {r.status_code}")
print(f"   Response: {r.text[:200]}")

print("\n" + "=" * 50)
