from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4, nullable=False)
    user_id: UUID = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    history: str = Field(default="[]", nullable=False) # JSON string of conversation turns
