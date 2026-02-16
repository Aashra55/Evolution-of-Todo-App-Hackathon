# backend/src/mcp_tools/update_task.py
from typing import Dict, Any, Optional, Union
from uuid import UUID
from sqlmodel import Session, select
from src.models.task import Task

def update_task(session: Session, user_id: UUID, task_id: Union[UUID, str, int], title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Updates an existing todo task for a user.
    """
    try:
        # Convert UUID to string for user_id
        user_id_str = str(user_id)
        
        # Convert task_id to int (handle UUID, string, or int)
        if isinstance(task_id, UUID):
            task_id_str = str(task_id).replace('-', '')
            try:
                task_id_int = int(task_id_str, 16) if len(task_id_str) > 10 else int(task_id_str)
            except ValueError:
                return {"status": "error", "message": f"Invalid task ID format: {task_id}. Expected integer."}
        elif isinstance(task_id, str):
            try:
                task_id_int = int(task_id)
            except ValueError:
                return {"status": "error", "message": f"Invalid task ID format: {task_id}. Expected integer."}
        elif isinstance(task_id, int):
            task_id_int = task_id
        else:
            return {"status": "error", "message": f"Invalid task ID type: {type(task_id)}. Expected integer."}
        
        task = session.exec(select(Task).where(Task.user_id == user_id_str, Task.id == task_id_int)).first()
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
                    "description": "The UUID of the user who owns the task. This is automatically provided - you should NOT ask the user for it or include it in your tool calls."
                },
                "task_id": {
                    "type": ["string", "integer"],
                    "description": "The ID of the task to be updated. This can be an integer ID or a string representation of the ID."
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
            "required": ["task_id"]  # user_id is automatically provided
        }
    }
}
