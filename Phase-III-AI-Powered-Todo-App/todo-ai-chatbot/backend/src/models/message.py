# backend/src/models/message.py
import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship

class Message(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True) # Foreign key to a User model if it existed
    conversation_id: UUID = Field(foreign_key="conversation.id")
    role: str # e.g., "user", "assistant", "tool"
    content: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    class Config:
        json_encoders = {
            datetime.datetime: lambda dt: dt.isoformat() + "Z"
        }

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if 'created_at' in data and data['created_at']:
            data['created_at'] = data['created_at'].isoformat() + "Z"
        return data

