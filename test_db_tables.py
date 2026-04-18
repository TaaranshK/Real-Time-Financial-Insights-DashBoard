#!/usr/bin/env python
"""Manual script to inspect table existence for the configured database."""

import os
from sqlalchemy import create_engine, inspect

DATABASE_URL = os.getenv("DATABASE_URL", "").strip() or "sqlite:///./financial_monitoring.db"


def run() -> None:
    """Run a simple table existence check."""
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("Tables in database:", tables)

    expected_tables = ["users", "portfolios", "holdings", "stocks", "market_analyses"]
    for table in expected_tables:
        print(f"  {table}: {'yes' if table in tables else 'no'}")

    engine.dispose()


if __name__ == "__main__":
    run()
