"""
auth_schema.py - Defines how Login data looks in API
====================================================

What this file does:
- LoginRequest: what user sends to login (email)
- TokenResponse: what we send back (JWT token)

How login works:
1. User sends email -> LoginRequest
2. Server checks user, creates token
3. Server sends back token -> TokenResponse
4. User uses this token for protected APIs
"""

# ============ IMPORTS ============
from pydantic import BaseModel


# ============ SCHEMA FOR LOGIN REQUEST ============
class LoginRequest(BaseModel):
    """
    What data user sends when trying to login.
    """
    
    # The email to login with
    email: str
    
    # The password
    password: str


# ============ SCHEMA FOR TOKEN RESPONSE ============
class TokenResponse(BaseModel):
    """
    What we send back after successful login.
    This contains the JWT token user needs for other APIs.
    """
    
    # The actual JWT token string
    access_token: str
    
    # Type of token (always "Bearer" for JWT)
    token_type: str
