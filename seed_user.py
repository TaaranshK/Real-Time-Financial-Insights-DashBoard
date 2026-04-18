"""
Seed database with a test user for demo purposes.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.user import User

def seed_test_user():
    """Add a test user to the database."""
    db: Session = SessionLocal()
    
    try:
        # Check if user already exists
        existing = db.query(User).filter(User.email == "demo@finvue.com").first()
        if existing:
            print("✓ User already exists: demo@finvue.com")
            print(f"  Password: Demo1234")
            return
        
        # Create new test user
        user = User(
            username="demo_user",
            email="demo@finvue.com",
            password="Demo1234",  # Plain text (not hashed in this system)
            first_name="Demo",
            last_name="User",
            phone="+1234567890",
            role="USER",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print("✓ Test user created successfully!")
        print(f"  Email: demo@finvue.com")
        print(f"  Password: Demo1234")
        print(f"  User ID: {user.id}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_user()
