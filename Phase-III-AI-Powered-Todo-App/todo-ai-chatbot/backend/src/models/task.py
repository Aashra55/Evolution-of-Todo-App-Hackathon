# backend/src/models/task.py
import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True) # Assuming user_id is also part of a composite primary key or indexed
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

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

# SQLModel does not directly support composite primary keys with default_factory for UUID
# For a composite primary key (user_id, id), we would need to manually set primary_key=True
# on both fields, and potentially handle default factory for UUID outside of Field if issues arise.
# For simplicity here, we'll assume 'id' is the primary key and 'user_id' is indexed.
