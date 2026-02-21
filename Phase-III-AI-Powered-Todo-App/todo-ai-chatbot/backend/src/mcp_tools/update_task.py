# backend/src/mcp_tools/update_task.py
from typing import Dict, Any, Optional, Union
from sqlmodel import Session, select
from src.models.task import Task
from src.mcp_tools.utils import find_task

def update_task(session: Session, user_id: int, task_id: Optional[int] = None, task_name: Optional[str] = None, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Updates an existing todo task for a user.
    """
    try:
        task = find_task(session, user_id, task_id, task_name)
        if not task:
            identifier = f"ID {task_id}" if task_id else f"name '{task_name}'"
            return {"status": "error", "message": f"Task with {identifier} not found for user {user_id}."}
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"status": "success", "message": f"Task '{task.title}' updated successfully.", "task_id": task.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"Failed to update task: {e}"}

# This dictionary defines the schema for the update_task tool,
# which can be used by the OpenAI Agent to understand how to call this function.
update_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Updates an existing todo task for a specific user. At least one of title, description, or completed must be provided. You can identify the task using either task_id or task_name.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user who owns the task. This is automatically provided - you should NOT ask the user for it or include it in your tool calls."
                },
                "task_id": {
                    "type": "integer",
                    "description": "(Optional) The ID of the task to be updated."
                },
                "task_name": {
                    "type": "string",
                    "description": "(Optional) The title or name of the task to be updated."
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
            "anyOf": [
                {"required": ["task_id"]},
                {"required": ["task_name"]}
            ]
        }
    }
}
