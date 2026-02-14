from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(sa_column=Column(String, index=True))
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None, index=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now()),
        default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now(), onupdate=func.now()),
        default_factory=datetime.utcnow
    )