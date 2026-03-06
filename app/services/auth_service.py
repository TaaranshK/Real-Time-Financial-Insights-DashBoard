"""
Authentication service using SQLAlchemy ORM.

Handles user registration, login, profile updates, and password reset flows.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils import jwt_util, otp_util, email_util

# In-memory token store: token -> user_id
TOKEN_STORE = {}


def generate_token():
    """Generate a unique access token."""
    return str(uuid.uuid4())


def store_token(token: str, user_id: int):
    """Store token mapping to user ID."""
    TOKEN_STORE[token] = user_id


def get_user_from_token(token: str, db: Session = None):
    """Get user from Bearer token."""
    if not db:
        raise ValueError("Database session required")
    
    user_id = TOKEN_STORE.get(token)
    if not user_id:
        return None
    
    return db.query(User).filter(User.id == user_id).first()


def register_user(username: str, email: str, password: str, first_name=None, 
                 last_name=None, phone=None, db: Session = None):
    """Register a new user."""
    if not db:
        raise ValueError("Database session required")
    
    existing_user = db.query(User).filter(User.email.ilike(email)).first()
    if existing_user:
        raise ValueError("Email already exists")
    
    user = User(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        role="USER"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(email: str, password: str, db: Session = None):
    """Authenticate user by email and password."""
    if not db:
        raise ValueError("Database session required")
    
    user = db.query(User).filter(User.email.ilike(email)).first()
    if not user or user.password != password:
        return None
    return user


def get_user_by_id(user_id: int, db: Session = None):
    """Get user by ID."""
    if not db:
        raise ValueError("Database session required")
    
    return db.query(User).filter(User.id == user_id).first()


def update_user_profile(user: User, updates: dict, db: Session = None) -> User:
    """Update user profile fields."""
    if not db:
        raise ValueError("Database session required")
    
    allowed_fields = {"username", "first_name", "last_name", "phone"}
    for field in allowed_fields:
        if field in updates and updates[field]:
            setattr(user, field, updates[field])
    
    db.commit()
    db.refresh(user)
    return user


def request_password_reset(email: str, db: Session = None) -> tuple[bool, str]:
    """
    Request password reset by email.
    Generates OTP and sends via email.
    
    Args:
        email: User email
        db: Database session
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not db:
        raise ValueError("Database session required")
    
    user = db.query(User).filter(User.email.ilike(email)).first()
    if not user:
        # Don't reveal if email exists for security
        return True, "If email exists, OTP will be sent"
    
    # Generate OTP
    otp_code = otp_util.generate_otp(user.id)
    
    # Send OTP via email
    email_sent = email_util.send_otp_email(user.email, otp_code, user.username)
    
    if not email_sent:
        return False, "Failed to send OTP email"
    
    # Update user: mark that reset was requested
    user.password_reset_requested_at = datetime.now(timezone.utc)
    user.password_reset_token_used = False
    db.commit()
    
    return True, "OTP sent to your email"


def verify_password_reset_otp(email: str, otp_code: str, db: Session = None) -> tuple[bool, str, str | None]:
    """
    Verify password reset OTP.
    
    Args:
        email: User email
        otp_code: 6-digit OTP code
        db: Database session
        
    Returns:
        Tuple of (success: bool, message: str, reset_token: str | None)
    """
    if not db:
        raise ValueError("Database session required")
    
    user = db.query(User).filter(User.email.ilike(email)).first()
    if not user:
        return False, "User not found", None
    
    # Verify OTP
    is_valid, message = otp_util.verify_otp(user.id, otp_code)
    
    if not is_valid:
        return False, message, None
    
    # Generate password reset JWT token
    reset_token = jwt_util.generate_password_reset_token(user.id, user.email)
    
    return True, "OTP verified. Use the reset token to set new password.", reset_token


def reset_password_with_token(reset_token: str, new_password: str, db: Session = None) -> tuple[bool, str]:
    """
    Reset password using JWT token from OTP verification.
    
    Args:
        reset_token: JWT password reset token
        new_password: New password
        db: Database session
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not db:
        raise ValueError("Database session required")
    
    # Verify token
    payload = jwt_util.verify_password_reset_token(reset_token)
    if not payload:
        return False, "Invalid or expired reset token"
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return False, "User not found"
    
    # Update password
    user.password = new_password
    user.password_reset_token_used = True
    db.commit()
    
    # Clear any remaining OTP
    otp_util.clear_otp(user.id)
    
    return True, "Password reset successfully"


def change_password(user: User, current_password: str, new_password: str, db: Session = None) -> tuple[bool, str]:
    """
    Change password for authenticated user.
    
    Args:
        user: User object
        current_password: Current password (must match)
        new_password: New password
        db: Database session
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not db:
        raise ValueError("Database session required")
    
    # Verify current password
    if user.password != current_password:
        return False, "Current password is incorrect"
    
    # Update password
    user.password = new_password
    db.commit()
    db.refresh(user)
    
    return True, "Password changed successfully"
