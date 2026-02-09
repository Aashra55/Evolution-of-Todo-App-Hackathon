from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(index=True)  # Assuming a User model for relationship, not yet defined
    description: str = Field(index=True, min_length=1, max_length=255)
    status: str = Field(default="pending", max_length=10) # Enforce enum 'pending', 'completed', 'deferred'
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    due_date: Optional[datetime] = Field(default=None)

    # Example of a simple Pydantic validation (more complex validation in service layer)
    @property
    def is_due_in_future(self) -> bool:
        if self.due_date:
            return self.due_date > datetime.utcnow()
        return True

    @property
    def is_status_valid(self) -> bool:
        return self.status in ["pending", "completed", "deferred"]

    def __repr__(self):
        return f"Todo(id={self.id}, description={self.description}, status={self.status}, user_id={self.user_id})"