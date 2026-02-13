from typing import Optional
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None, index=True)
    completed: bool = Field(default=False)