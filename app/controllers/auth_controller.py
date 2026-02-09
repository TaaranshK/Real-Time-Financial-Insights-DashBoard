"""
auth_controller.py - handles user login

basically: user gives email -> we give them a token
if they're new, we just create an account for them
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.user_model import User
from ..schemas.auth_schema import LoginRequest, TokenResponse
from ..utils.jwt_util import create_jwt_token
from ..utils.password_util import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    """get a db connection, close it when we're done"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=TokenResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """
    POST /auth/login
    send: {"email": "user@example.com", "password": "yourpassword"}
    get back: {"access_token": "...", "token_type": "Bearer"}
    """
    
    # check if this email exists
    user = db.query(User).filter(User.email == request.email).first()
    
    # user not found
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # verify password - check if password is set
    if not user.hashed_password:
        raise HTTPException(status_code=401, detail="Please register first - no password set")
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # make a token with their info
    token = create_jwt_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    return {"access_token": token, "token_type": "Bearer"}
