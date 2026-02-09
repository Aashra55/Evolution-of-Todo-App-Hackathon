from typing import List, Annotated, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel

from ...models.todo import Todo
from ...models.user import User
from ...services.todo_service import TodoService, TodoNotFoundError
from ..dependencies import get_todo_service, verify_todo_ownership
from ..auth import get_authenticated_user


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(get_authenticated_user)] # All todo endpoints are protected
)


class TodoCreate(BaseModel):
    description: str
    due_date: Optional[datetime] = None


class TodoUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None


class TodoRead(BaseModel):
    id: UUID
    user_id: UUID
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo_endpoint(
    todo_data: TodoCreate,
    current_user: Annotated[User, Depends(get_authenticated_user)],
    todo_service: Annotated[TodoService, Depends(get_todo_service)]
):
    try:
        todo = todo_service.create_todo(current_user.id, todo_data.description, todo_data.due_date)
        return todo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo_endpoint(
    todo: Annotated[Todo, Depends(verify_todo_ownership)] # Ownership verified by dependency
):
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo_endpoint(
    todo_update: TodoUpdate,
    todo: Annotated[Todo, Depends(verify_todo_ownership)], # Ownership verified by dependency
    todo_service: Annotated[TodoService, Depends(get_todo_service)]
):
    try:
        updated_todo = todo_service.update_todo(
            todo.user_id, todo.id,
            todo_update.description, todo_update.status, todo_update.due_date
        )
        return updated_todo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_endpoint(
    todo: Annotated[Todo, Depends(verify_todo_ownership)], # Ownership verified by dependency
    todo_service: Annotated[TodoService, Depends(get_todo_service)]
):
    todo_service.delete_todo(todo.user_id, todo.id)
    return


@router.get("/user/{user_id}", response_model=List[TodoRead])
def list_todos_for_user_endpoint(
    user_id: UUID,
    current_user: Annotated[User, Depends(get_authenticated_user)],
    todo_service: Annotated[TodoService, Depends(get_todo_service)]
):
    if str(user_id) != str(current_user.id): # Ensure user can only list their own todos
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access other users' todos"
        )
    todos = todo_service.get_todos_by_user(user_id)
    return todos
