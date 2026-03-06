#!/usr/bin/env python
"""Inspect existing database schema."""
from sqlalchemy import create_engine, text, inspect

# Connect to database
engine = create_engine('postgresql://postgres:Guddiguddi13@localhost:5432/financial_db')
inspector = inspect(engine)

# List all tables with columns
for table_name in inspector.get_table_names():
    print(f"\nTable: {table_name}")
    columns = inspector.get_columns(table_name)
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")

engine.dispose()
