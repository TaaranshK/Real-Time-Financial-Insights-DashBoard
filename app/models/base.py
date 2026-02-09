"""
base.py - The foundation for all database tables
===================================================

What this file does:
- Creates a "Base" class that all our models inherit from
- Think of Base like a parent class for all tables


"""

from sqlalchemy.ext.declarative import declarative_base

# This creates the base class for all our database models
# Every table we create will inherit from this Base
Base = declarative_base()
