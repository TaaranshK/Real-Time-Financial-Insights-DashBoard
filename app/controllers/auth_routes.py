"""
Auth routes - POST /register, /login, GET /profile, PUT /profile
Also includes password reset endpoints: /forgot-password, /verify-otp, /reset-password
"""

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.models.schemas import (
    LoginRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
)
from app.database import get_db
from app.services.auth_service import (
    authenticate_user,
    generate_token,
    get_user_from_token,
    register_user,
    store_token,
    update_user_profile,
    request_password_reset,
    verify_password_reset_otp,
    reset_password_with_token,
    change_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    """Dependency to extract user from Bearer token."""
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    token = parts[1].strip()
    user = get_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    return user


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        user = register_user(
            payload.username,
            payload.email,
            payload.password,
            payload.first_name,
            payload.last_name,
            payload.phone,
            db
        )
        return {
            "message": "User registered successfully",
            "user": user.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user = authenticate_user(payload.email, payload.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = generate_token()
    refresh_token = generate_token()
    store_token(access_token, user.id)
    
    return {
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        },
    }


@router.get("/profile")
def get_profile(user=Depends(get_current_user)):
    """Get current user profile."""
    return {"message": "Profile retrieved", "user": user.to_dict()}


@router.put("/profile")
def update_profile(payload: ProfileUpdateRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Update user profile."""
    updates = payload.model_dump(exclude_none=True)
    updated = update_user_profile(user, updates, db)
    return {"message": "Profile updated", "user": updated.to_dict()}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request password reset.
    Generates and sends OTP to user's email.
    
    Returns: {"message": str, "success": bool}
    """
    success, message = request_password_reset(payload.email, db)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    return {"success": success, "message": message}


@router.post("/verify-otp")
def verify_otp(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    """
    Verify password reset OTP.
    Returns JWT reset token if OTP is valid.
    
    Returns: {"message": str, "success": bool, "reset_token": str | None}
    """
    success, message, reset_token = verify_password_reset_otp(payload.email, payload.otp_code, db)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    return {
        "success": success,
        "message": message,
        "reset_token": reset_token
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset password using JWT token from OTP verification.
    
    Returns: {"message": str, "success": bool}
    """
    success, message = reset_password_with_token(payload.reset_token, payload.new_password, db)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    return {"success": success, "message": message}


@router.post("/change-password")
def change_pwd(payload: ChangePasswordRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Change password for authenticated user.
    Requires current password and new password.
    
    Returns: {"message": str, "success": bool}
    """
    success, message = change_password(user, payload.current_password, payload.new_password, db)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    return {"success": success, "message": message}
