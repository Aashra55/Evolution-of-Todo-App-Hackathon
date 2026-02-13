from typing import Optional
from sqlmodel import Field, SQLModel

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(index=True)
    text: str
    sender: str # e.g., "user" or "ai"