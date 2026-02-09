from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlmodel import Session, select

from ..models.todo import Todo
from .database import get_session


class TodoNotFoundError(Exception):
    pass


class TodoService:
    def __init__(self, session: Session = get_session()):
        self.session = session

    def create_todo(self, user_id: UUID, description: str, due_date: Optional[datetime] = None) -> Todo:
        if not description:
            raise ValueError("Description cannot be empty.")
        if due_date and due_date <= datetime.utcnow():
            raise ValueError("Due date must be in the future.")

        todo = Todo(user_id=user_id, description=description, due_date=due_date)
        with self.session:
            self.session.add(todo)
            self.session.commit()
            self.session.refresh(todo)
        return todo

    def get_todo(self, user_id: UUID, todo_id: UUID) -> Todo:
        with self.session:
            todo = self.session.get(Todo, todo_id)
            if not todo or todo.user_id != user_id:
                raise TodoNotFoundError(f"Todo with ID {todo_id} not found for user {user_id}.")
            return todo

    def get_todos_by_user(self, user_id: UUID) -> List[Todo]:
        with self.session:
            statement = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at)
            todos = self.session.exec(statement).all()
            return todos

    def update_todo(self, user_id: UUID, todo_id: UUID, new_description: Optional[str] = None, new_status: Optional[str] = None, new_due_date: Optional[datetime] = None) -> Todo:
        with self.session:
            todo = self.session.get(Todo, todo_id)
            if not todo or todo.user_id != user_id:
                raise TodoNotFoundError(f"Todo with ID {todo_id} not found for user {user_id}.")

            if new_description is not None:
                if not new_description:
                    raise ValueError("Description cannot be empty.")
                todo.description = new_description
            if new_status is not None:
                if new_status not in ["pending", "completed", "deferred"]:
                    raise ValueError(f"Invalid status: {new_status}.")
                todo.status = new_status
            if new_due_date is not None:
                if new_due_date <= datetime.utcnow():
                    raise ValueError("Due date must be in the future.")
                todo.due_date = new_due_date
            
            todo.updated_at = datetime.utcnow() # Update timestamp on change

            self.session.add(todo)
            self.session.commit()
            self.session.refresh(todo)
        return todo

    def delete_todo(self, user_id: UUID, todo_id: UUID):
        with self.session:
            todo = self.session.get(Todo, todo_id)
            if not todo or todo.user_id != user_id:
                raise TodoNotFoundError(f"Todo with ID {todo_id} not found for user {user_id}.")
            self.session.delete(todo)
            self.session.commit()
