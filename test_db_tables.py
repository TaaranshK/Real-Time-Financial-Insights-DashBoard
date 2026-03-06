#!/usr/bin/env python
"""Test database schema."""
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

# Connect to database
engine = create_engine('postgresql://postgres:Guddiguddi13@localhost:5432/financial_db')
inspector = inspect(engine)

# Get all tables
tables = inspector.get_table_names()
print("Tables in database:", tables)

# Check if key tables exist
needed_tables = ['user', 'portfolio', 'holding', 'stock', 'market_analysis']
for table in needed_tables:
    exists = table in tables
    print(f"  {table}: {'✓' if exists else '✗'}")

# If tables don't exist, create them
if not tables:
    print("\nNo tables found. Need to run migrations.")
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables now:", tables)
else:
    print("\nTables already exist!")

engine.dispose()
