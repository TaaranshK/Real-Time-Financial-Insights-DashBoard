"""

What this file does:
1. Creates a connection to PostgreSQL database
2. Provides a way for other files to talk to database


"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "postgresql://postgres:Guddiguddi13%40@localhost:5432/financial_db"



# This creates the actual connection to database basically acts as a bridge between Python and Postgrsql

engine = create_engine(DATABASE_URL)



# SessionLocal is like a factory that creates database sessions
# Each session is like opening Excel - you make changes, then save and close
SessionLocal = sessionmaker(
    autocommit=False,   # We will manually commit changes
    autoflush=False,    # Don't automatically send changes
    bind=engine         # Connect to our database engine
)