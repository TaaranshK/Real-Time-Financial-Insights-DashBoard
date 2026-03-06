"""
Database configuration and session management.
Uses SQLite for development, PostgreSQL for production.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Store AND Configure URL  
# PostgreSQL connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Guddiguddi13@localhost:5432/financial_db"
)

#Create Database Engine
engine = create_engine(DATABASE_URL)

# Create Database Session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Handle The Database Injection
def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
