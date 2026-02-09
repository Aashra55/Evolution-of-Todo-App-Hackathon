from typing import Optional, List
from uuid import UUID
from datetime import datetime

from fastapi import Depends
from sqlmodel import Session

from backend.src.services.todo_service import TodoService, TodoNotFoundError
from backend.src.services.database import get_session
from backend.src.mcp_server import register_tool
from backend.src.models.todo import Todo # Import Todo model for type hints


# Dependency for getting TodoService within MCP tools
def get_mcp_todo_service(session: Session = Depends(get_session)) -> TodoService:
    return TodoService(session)

@register_tool("create_todo")
async def create_todo_tool(
    user_id: str, # UUID passed as str from AI Agent
    description: str,
    due_date: Optional[str] = None, # datetime passed as str from AI Agent
    todo_service: TodoService = Depends(get_mcp_todo_service)
) -> dict:
    """
    Creates a new todo item for the specified user.
    Args:
        user_id (str): The ID of the user creating the todo.
        description (str): The description of the todo item.
        due_date (Optional[str]): The optional due date for the todo in ISO 8601 format.
    Returns:
        dict: The created todo item's details.
    """
    try:
        parsed_user_id = UUID(user_id)
        parsed_due_date = datetime.fromisoformat(due_date) if due_date else None
        
        todo = todo_service.create_todo(parsed_user_id, description, parsed_due_date)
        return todo.dict()
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@register_tool("get_todo")
async def get_todo_tool(
    user_id: str,
    todo_id: str,
    todo_service: TodoService = Depends(get_mcp_todo_service)
) -> dict:
    """
    Retrieves a specific todo item by its ID for a given user.
    Args:
        user_id (str): The ID of the user owning the todo.
        todo_id (str): The ID of the todo item to retrieve.
    Returns:
        dict: The todo item's details.
    """
    try:
        parsed_user_id = UUID(user_id)
        parsed_todo_id = UUID(todo_id)
        todo = todo_service.get_todo(parsed_user_id, parsed_todo_id)
        return todo.dict()
    except TodoNotFoundError:
        return {"error": f"Todo with ID {todo_id} not found for user {user_id}."}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@register_tool("list_todos_by_user")
async def list_todos_by_user_tool(
    user_id: str,
    todo_service: TodoService = Depends(get_mcp_todo_service)
) -> List[dict]:
    """
    Lists all todo items for a specific user.
    Args:
        user_id (str): The ID of the user whose todos to list.
    Returns:
        List[dict]: A list of todo items.
    """
    try:
        parsed_user_id = UUID(user_id)
        todos = todo_service.get_todos_by_user(parsed_user_id)
        return [todo.dict() for todo in todos]
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@register_tool("update_todo")
async def update_todo_tool(
    user_id: str,
    todo_id: str,
    new_description: Optional[str] = None,
    new_status: Optional[str] = None,
    new_due_date: Optional[str] = None,
    todo_service: TodoService = Depends(get_mcp_todo_service)
) -> dict:
    """
    Updates an existing todo item for a given user.
    Args:
        user_id (str): The ID of the user owning the todo.
        todo_id (str): The ID of the todo item to update.
        new_description (Optional[str]): The new description for the todo.
        new_status (Optional[str]): The new status (e.g., 'completed', 'pending', 'deferred').
        new_due_date (Optional[str]): The new due date in ISO 8601 format.
    Returns:
        dict: The updated todo item's details.
    """
    try:
        parsed_user_id = UUID(user_id)
        parsed_todo_id = UUID(todo_id)
        parsed_new_due_date = datetime.fromisoformat(new_due_date) if new_due_date else None

        todo = todo_service.update_todo(
            parsed_user_id, parsed_todo_id, new_description, new_status, parsed_new_due_date
        )
        return todo.dict()
    except TodoNotFoundError:
        return {"error": f"Todo with ID {todo_id} not found for user {user_id}."}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@register_tool("delete_todo")
async def delete_todo_tool(
    user_id: str,
    todo_id: str,
    todo_service: TodoService = Depends(get_mcp_todo_service)
) -> dict:
    """
    Deletes a specific todo item for a given user.
    Args:
        user_id (str): The ID of the user owning the todo.
        todo_id (str): The ID of the todo item to delete.
    Returns:
        dict: A success message or error.
    """
    try:
        parsed_user_id = UUID(user_id)
        parsed_todo_id = UUID(todo_id)
        todo_service.delete_todo(parsed_user_id, parsed_todo_id)
        return {"message": f"Todo with ID {todo_id} deleted successfully."}
    except TodoNotFoundError:
        return {"error": f"Todo with ID {todo_id} not found for user {user_id}."}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
