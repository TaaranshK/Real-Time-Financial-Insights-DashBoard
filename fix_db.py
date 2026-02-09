"""Fix the users table - make hashed_password nullable"""
from sqlalchemy import text
from app.database import engine

# Run ALTER TABLE to make hashed_password nullable
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL;"))
    conn.commit()
    print("Fixed! hashed_password is now nullable.")
