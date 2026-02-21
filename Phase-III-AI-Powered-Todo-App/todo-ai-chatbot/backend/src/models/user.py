# backend/src/models/user.py
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None, index=True, unique=True)
    hashed_password: str

    tasks: List["Task"] = Relationship(back_populates="user")
    messages: List["Message"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")
