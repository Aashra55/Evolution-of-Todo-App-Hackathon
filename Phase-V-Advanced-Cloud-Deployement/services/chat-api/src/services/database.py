from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database URL from environment variable or default to a local SQLite for simplicity
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./todo.db") # Using SQLite for simplicity, replace with PostgreSQL for actual deployment

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # This should be imported from models.py if models are defined elsewhere

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ensure tables are created if using SQLite for local dev (remove for actual DB migration tools)
# Base.metadata.create_all(bind=engine)
