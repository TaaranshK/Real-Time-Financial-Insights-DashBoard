#!/usr/bin/env python
"""Drop old tables and create new ORM schema."""
from sqlalchemy import create_engine, text
from app.database import Base

# Import all models to register them with Base
from app.models.user import User
from app.models.portfolio_model import Portfolio
from app.models.holding import Holding
from app.models.stock import Stock
from app.models.market_analysis import MarketAnalysis

# Connect to database
DATABASE_URL = 'postgresql://postgres:Guddiguddi13@localhost:5432/financial_db'
engine = create_engine(DATABASE_URL)

print("Dropping existing tables...")
# Drop existing tables that don't match our ORM
with engine.begin() as connection:
    connection.execute(text('DROP TABLE IF EXISTS market_prices CASCADE'))
    connection.execute(text('DROP TABLE IF EXISTS alerts CASCADE'))
    connection.execute(text('DROP TABLE IF EXISTS portfolio CASCADE'))
    connection.execute(text('DROP TABLE IF EXISTS users CASCADE'))
    connection.commit()
    print("Old tables dropped.")

print("\nCreating new ORM tables...")
# Create new tables based on ORM models
Base.metadata.create_all(bind=engine)
print("New tables created!")

print("\nVerifying schema...")
from sqlalchemy import inspect
inspector = inspect(engine)
for table_name in sorted(inspector.get_table_names()):
    print(f"\n  Table: {table_name}")
    columns = inspector.get_columns(table_name)
    for col in columns:
        print(f"    - {col['name']}: {col['type']}")

engine.dispose()
print("\nDone!")
