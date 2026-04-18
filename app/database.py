"""
Database configuration and session management.

Uses SQLite by default for local development, and respects DATABASE_URL when set.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Use SQLite by default so backend works without requiring local PostgreSQL.
DATABASE_URL = os.getenv("DATABASE_URL", "").strip() or "sqlite:///./financial_monitoring.db"

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
