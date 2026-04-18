#!/usr/bin/env python
"""Drop and recreate ORM schema for the configured database URL."""
from app.database import Base, engine

# Import all models to register them with Base
from app.models.user import User
from app.models.portfolio_model import Portfolio
from app.models.holding import Holding
from app.models.stock import Stock
from app.models.market_analysis import MarketAnalysis

print("Dropping existing ORM tables...")
Base.metadata.drop_all(bind=engine)
print("Existing ORM tables dropped.")

print("\nCreating new ORM tables...")
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
