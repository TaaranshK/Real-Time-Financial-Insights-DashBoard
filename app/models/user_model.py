"""

What this file does:
- Defines the "users" table structure
- Each row in this table = one user


"""

# ============ IMPORTS ============
from sqlalchemy import Column, Integer, String
from .base import Base


#  USER TABLE 
class User(Base):
    
    # Name of the table in database
    __tablename__ = "users"

    # Column 1: id - every user gets a unique number
    # primary_key=True means this is the main identifier
    # index=True makes searching faster
    id = Column(Integer, primary_key=True, index=True)
    
    # Column 2: email - the user's email address
    # unique=True means no two users can have same email
    email = Column(String, unique=True, index=True)
    
    # Column 3: Hashed password (optional for email-only login)
    hashed_password = Column(String, nullable=True)

    # Column 4: role - what type of user ("user" or "admin")
    role = Column(String)
