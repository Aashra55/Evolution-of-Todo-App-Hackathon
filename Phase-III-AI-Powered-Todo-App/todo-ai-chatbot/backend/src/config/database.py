# backend/src/config/database.py
import os
from typing import Generator

from sqlmodel import create_engine, Session, SQLModel

# Import your models here to ensure they are registered with SQLModel metadata
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables based on SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session