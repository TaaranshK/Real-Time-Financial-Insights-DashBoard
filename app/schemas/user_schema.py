"""


Schemas:
- UserRegister: used during registration
- UserLogin: used during login
- UserResponse: used when sending user data back
"""

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """
    Data required to register a new user.
    """
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Data required to login a user.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Data returned to client .
    """
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True
