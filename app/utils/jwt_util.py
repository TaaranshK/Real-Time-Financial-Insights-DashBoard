
"""
JWT Token Utility - Simplified for password reset and email verification.

Generic token generation and verification with configurable purpose and expiration.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"


def _create_token(user_id: int, email: str, purpose: str, hours: int) -> str:
    """
    Generic token creation (Internal use).
    
    Args:
        user_id: User ID to encode
        email: User email to encode
        purpose: Token purpose (e.g., "password_reset", "email_verification")
        hours: Token expiration in hours
        
    Returns:
        JWT token string
    """
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "email": email,
        "purpose": purpose,
        "iat": now,
        "exp": now + timedelta(hours=hours),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def _verify_token(token: str, expected_purpose: str) -> Optional[Dict[str, Any]]:
    """
    Generic token verification (Internal use).
    
    Args:
        token: JWT token string
        expected_purpose: Expected token purpose for validation
        
    Returns:
        Decoded payload if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("purpose") != expected_purpose:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        print(f"[JWT] {expected_purpose} token expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"[JWT] Invalid token: {e}")
        return None


# === PASSWORD RESET TOKENS ===

def generate_password_reset_token(user_id: int, email: str) -> str:
    """Generate a 1-hour password reset token."""
    return _create_token(user_id, email, "password_reset", hours=1)


def verify_password_reset_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a password reset token."""
    return _verify_token(token, "password_reset")


# === EMAIL VERIFICATION TOKENS ===

def generate_email_verification_token(user_id: int, email: str) -> str:
    """Generate a 24-hour email verification token."""
    return _create_token(user_id, email, "email_verification", hours=24)


def verify_email_verification_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify an email verification token."""
    return _verify_token(token, "email_verification")
