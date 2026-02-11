# backend/src/mcp_tools/update_task.py
from typing import Dict, Any, Optional
from uuid import UUID
from sqlmodel import Session, select
from src.models.task import Task

def update_task(session: Session, user_id: UUID, task_id: UUID, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Updates an existing todo task for a user.
    """
    try:
        task = session.exec(select(Task).where(Task.user_id == user_id, Task.id == task_id)).first()
        if not task:
            return {"status": "error", "message": f"Task with ID {task_id} not found for user {user_id}."}
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"status": "success", "message": f"Task '{task.title}' updated successfully.", "task_id": str(task.id)}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"Failed to update task: {e}"}

# This dictionary defines the schema for the update_task tool,
# which can be used by the OpenAI Agent to understand how to call this function.
update_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Updates an existing todo task for a specific user. At least one of title, description, or completed must be provided.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The UUID of the user who owns the task."
                },
                "task_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The UUID of the task to be updated."
                },
                "title": {
                    "type": "string",
                    "description": "(Optional) The new title for the task."
                },
                "description": {
                    "type": "string",
                    "description": "(Optional) The new detailed description for the task."
                },
                "completed": {
                    "type": "boolean",
                    "description": "(Optional) The new completion status for the task (True for completed, False for pending)."
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
