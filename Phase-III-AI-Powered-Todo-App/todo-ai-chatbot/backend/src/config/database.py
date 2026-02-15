# backend/src/config/database.py
import os
from typing import Generator
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

# Import your models here to ensure they are registered with SQLModel metadata
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todo_app.db")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Create database tables based on SQLModel metadata."""
    # In production, you'd want to use proper migrations (e.g., with Alembic)
    # instead of creating tables directly on startup.
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session