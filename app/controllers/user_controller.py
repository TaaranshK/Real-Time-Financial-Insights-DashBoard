"""
user_controller.py - Handles User APIs
=======================================

What this file does:
- Create new user: POST /users/
- Get all users: GET /users/
- Get my profile: GET /users/me (requires login)

These are the APIs for managing users.
"""

# ============ IMPORTS ============
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.user_model import User
from ..schemas.user_schema import UserRegister, UserResponse
from ..auth.auth_validate import auth_validate
from ..utils.password_util import hash_password


# ============ CREATE ROUTER ============
# All routes in this file will start with /users
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ============ DATABASE SESSION ============
def get_db():
    """
    Creates a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============ API 1: CREATE USER ============
@router.post("/", response_model=UserResponse)
def create_user(user: UserRegister, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    URL: POST /users/
    Body: {"email": "user@example.com", "password": "123456"}
    Returns: the created user
    """
    
    # Step 1: Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Step 2: Create new user with hashed password
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user"
    )
    
    # Step 3: Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ============ API 2: GET ALL USERS ============
@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users from database.
    
    URL: GET /users/
    Returns: list of all users
    """
    return db.query(User).all()


# ============ API 3: GET MY PROFILE ============
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user=Depends(auth_validate),
    db: Session = Depends(get_db)
):
    """
    Get profile of logged-in user.
    Requires JWT token in Authorization header.
    
    URL: GET /users/me
    Header: Authorization: Bearer <token>
    Returns: the user's profile
    """
    
    # Step 1: Get user_id from JWT token
    user_id = current_user["user_id"]

    # Step 2: Find user in database
    user = db.query(User).filter(User.id == user_id).first()

    # Step 3: If user not found (shouldn't happen)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 4: Return user profile
    return user
