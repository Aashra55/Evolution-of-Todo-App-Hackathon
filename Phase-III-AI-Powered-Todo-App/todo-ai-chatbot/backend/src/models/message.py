from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.sql import func

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str = Field(sa_column=Column(String))  # "user", "assistant", "tool"
    content: str = Field(sa_column=Column(String))
    created_at: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now()),
        default_factory=datetime.utcnow
    )

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="messages")

    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")