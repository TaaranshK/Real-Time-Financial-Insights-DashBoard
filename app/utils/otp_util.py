

import random
import string
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional

# In-memory OTP store: {user_id: {"code": "123456", "created_at": datetime, "attempts": 0}}
OTP_STORE = {}
OTP_LENGTH = 6
OTP_EXPIRATION_MINUTES = 10
MAX_OTP_ATTEMPTS = 5


def generate_otp(user_id: int) -> str:
    """
    Generate a random 6-digit OTP for the user.
    
    Args:
        user_id: User ID to generate OTP for
        
    Returns:
        6-digit OTP code as string
    """
    otp_code = "".join(random.choices(string.digits, k=OTP_LENGTH))
    
    # Store OTP with timestamp and attempt counter
    OTP_STORE[user_id] = {
        "code": otp_code,
        "created_at": datetime.now(timezone.utc),
        "attempts": 0,
    }
    
    print(f"[OTP] Generated OTP for user {user_id}: {otp_code}")
    return otp_code


def verify_otp(user_id: int, provided_code: str) -> Tuple[bool, str]:
    """
    Verify the provided OTP against stored OTP.
    
    Args:
        user_id: User ID to verify OTP for
        provided_code: OTP code provided by user
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if user_id not in OTP_STORE:
        return False, "No OTP found for this user. Request a new one."
    
    otp_data = OTP_STORE[user_id]
    
    # Check if OTP has expired
    created_at = otp_data["created_at"]
    if datetime.now(timezone.utc) - created_at > timedelta(minutes=OTP_EXPIRATION_MINUTES):
        del OTP_STORE[user_id]
        return False, "OTP has expired. Request a new one."
    
    # Check attempts
    if otp_data["attempts"] >= MAX_OTP_ATTEMPTS:
        del OTP_STORE[user_id]
        return False, "Too many failed attempts. Request a new OTP."
    
    # Verify code
    if otp_data["code"] != provided_code:
        otp_data["attempts"] += 1
        remaining = MAX_OTP_ATTEMPTS - otp_data["attempts"]
        return False, f"Invalid OTP. {remaining} attempts remaining."
    
    # OTP is valid - delete it (single use)
    del OTP_STORE[user_id]
    print(f"[OTP] OTP verified successfully for user {user_id}")
    return True, "OTP verified successfully"


def is_otp_valid(user_id: int) -> bool:
    """
    Check if a valid OTP exists for the user.
    
    Args:
        user_id: User ID to check
        
    Returns:
        True if valid OTP exists, False otherwise
    """
    if user_id not in OTP_STORE:
        return False
    
    otp_data = OTP_STORE[user_id]
    created_at = otp_data["created_at"]
    
    # Check if not expired
    if datetime.now(timezone.utc) - created_at > timedelta(minutes=OTP_EXPIRATION_MINUTES):
        del OTP_STORE[user_id]
        return False
    
    return True


def clear_otp(user_id: int) -> None:
    """
    Clear OTP for a user (after successful verification or manual clear).
    
    Args:
        user_id: User ID to clear OTP for
    """
    if user_id in OTP_STORE:
        del OTP_STORE[user_id]
        print(f"[OTP] Cleared OTP for user {user_id}")
