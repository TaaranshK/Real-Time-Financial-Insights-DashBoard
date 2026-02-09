"""auth_validate.py - checks if request has valid JWT token"""

from fastapi import Header, HTTPException
from ..utils.jwt_util import decode_jwt_token


def auth_validate(authorization: str = Header(...)):
    """validates JWT from Authorization header, returns user data or 401"""

    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid format. Use: Bearer <token>")

    token = authorization.split(" ")[1]
    user_data = decode_jwt_token(token)

    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_data
