# backend/src/models/conversation.py
import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship

class Conversation(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True) # Foreign key to a User model if it existed
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    # Messages in this conversation
    messages: list["Message"] = Relationship(back_populates="conversation")

    class Config:
        json_encoders = {
            datetime.datetime: lambda dt: dt.isoformat() + "Z"
        }

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if 'created_at' in data and data['created_at']:
            data['created_at'] = data['created_at'].isoformat() + "Z"
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = data['updated_at'].isoformat() + "Z"
        return data

