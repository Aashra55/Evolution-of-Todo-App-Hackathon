from typing import Optional
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    password: str


class UserPublic(SQLModel):
    id: int
    email: str


class UserLogin(SQLModel):
    email: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    email: Optional[str] = None


class TaskBase(SQLModel):
    description: str
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskPublic(TaskBase):
    id: int
    owner_id: int
