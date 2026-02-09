from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from ..models.user import User
from ..services.database import get_session
from ..services.todo_service import TodoService, TodoNotFoundError
from .auth import get_authenticated_user


def get_todo_service(session: Session = Depends(get_session)) -> TodoService:
    return TodoService(session)


async def verify_todo_ownership(
    todo_id: UUID,
    current_user: User = Depends(get_authenticated_user),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        todo = todo_service.get_todo(current_user.id, todo_id)
        if todo.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this todo"
            )
        return todo # Return the todo if ownership is verified
    except TodoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
