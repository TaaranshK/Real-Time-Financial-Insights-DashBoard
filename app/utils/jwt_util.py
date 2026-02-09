"""
jwt_util.py - Handles JWT Token Creation and Validation
========================================================

What this file does:
- Creates JWT tokens (for login)
- Decodes JWT tokens (to check if user is logged in)

W
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError



# Secret key used to sign tokens (keep this private!)
SECRET_KEY = "lead-nurturing-style-secret"

# Algorithm used for encryption
ALGORITHM = "HS256"

# Token expires after 60 minutes
TOKEN_EXPIRY_MINUTES = 60



def create_jwt_token(data: dict):
    """
    Creates a JWT token with user data.
    
    Input: {"user_id": 1, "email": "user@example.com", "role": "user"}
    Output: "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
    """
    
    # Step 1: Copy the data (don't modify original)
    payload = data.copy()

    # Step 2: Calculate expiry time (now + 60 minutes)
    expiry_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    
    # Step 3: Add expiry to payload
    payload["exp"] = expiry_time

    # Step 4: Generate the token string
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token



def decode_jwt_token(token: str):
    """
    Decodes a JWT token and returns the data inside.
    Returns None if token is invalid or expired.
    
    Input: "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
    Output: {"user_id": 1, "email": "user@example.com", "role": "user"}
    """
    
    try:
        # Try to decode the token
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    
    except JWTError:
        # Token is invalid or expired
        return None
