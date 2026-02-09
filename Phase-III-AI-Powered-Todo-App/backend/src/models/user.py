from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4, nullable=False)
    username: str = Field(unique=True, index=True)
    hashed_password: str # This would store a hashed password
    email: Optional[str] = Field(default=None, unique=True, index=True)

    # In a real app, you'd add methods for password hashing/verification
