# backend/src/mcp_tools/add_task.py
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session
from src.models.task import Task

def add_task(session: Session, user_id: UUID, title: str, description: str = None) -> Dict[str, Any]:
    """
    Adds a new todo task for a user.
    """
    try:
        new_task = Task(user_id=user_id, title=title, description=description)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return {"status": "success", "message": f"Task '{new_task.title}' added successfully.", "task_id": str(new_task.id)}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"Failed to add task: {e}"}

# This dictionary defines the schema for the add_task tool,
# which can be used by the OpenAI Agent to understand how to call this function.
add_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Adds a new todo task for a specific user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The UUID of the user for whom the task is being added."
                },
                "title": {
                    "type": "string",
                    "description": "The title or short description of the new task."
                },
                "description": {
                    "type": "string",
                    "description": "(Optional) A detailed description of the task."
                }
            },
            "required": ["user_id", "title"]
        }
    }
}
