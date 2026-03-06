"""
Pytest configuration and fixtures.

Uses SQLite for testing instead of PostgreSQL for convenience.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app import database
from app.database import Base
from app.main import app


@pytest.fixture(scope="function")
def test_db_session():
    """Create a fresh test database for each test."""
    # Use SQLite in memory for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db_session = TestingSessionLocal()
    
    yield db_session
    
    db_session.close()


@pytest.fixture
def client(test_db_session):
    """Create a FastAPI test client with database dependency override."""
    def override_get_db():
        yield test_db_session
    
    app.dependency_overrides[database.get_db] = override_get_db
    
    client = TestClient(app)
    
    yield client
    
    # Cleanup
    app.dependency_overrides.clear()
