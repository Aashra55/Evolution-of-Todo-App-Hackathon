# backend/src/config/database.py

import os
from typing import Generator

from sqlmodel import create_engine, Session

# Environment variable for database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:password@localhost:5432/todo_db")

# Create the engine
# For PostgreSQL, use "postgresql+psycopg://"
# For SQLite, use "sqlite://./database.db"
# For async, use "postgresql+asyncpg://" or "sqlite+aiosqlite://"
engine = create_engine(DATABASE_URL, echo=True) # echo=True for SQL logging

def create_db_and_tables():
    # This function is typically used with Alembic for migrations,
    # but can be used for initial table creation if not using migrations yet.
    # from backend.src.models.todo import Task, Conversation, Message # Import models to make them known to SQLModel
    # SQLModel.metadata.create_all(engine)
    pass # Managed by Alembic migrations

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
