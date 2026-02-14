from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.sql import func

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(sa_column=Column(String, index=True))
    conversation_id: int = Field(sa_column=Column(Integer, index=True))
    role: str = Field(sa_column=Column(String))  # "user", "assistant", "tool"
    content: str = Field(sa_column=Column(String))
    created_at: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now()),
        default_factory=datetime.utcnow
    )