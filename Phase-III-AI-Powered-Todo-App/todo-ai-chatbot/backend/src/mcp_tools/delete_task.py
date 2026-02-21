# backend/src/mcp_tools/delete_task.py
from typing import Dict, Any, Union, Optional
from sqlmodel import Session, select
from src.models.task import Task
from src.mcp_tools.utils import find_task

def delete_task(session: Session, user_id: int, task_id: Optional[int] = None, task_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Deletes a todo task for a user.
    """
    try:
        task = find_task(session, user_id, task_id, task_name)
        if not task:
            identifier = f"ID {task_id}" if task_id else f"name '{task_name}'"
            return {"status": "error", "message": f"Task with {identifier} not found for user {user_id}."}
        
        session.delete(task)
        session.commit()
        return {"status": "success", "message": f"Task '{task.title}' deleted successfully.", "task_id": task.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"Failed to delete task: {e}"}

delete_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Deletes a specific todo task for a user. You can provide either task_id or task_name.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user who owns the task. This is automatically provided - you should NOT ask the user for it or include it in your tool calls."
                },
                "task_id": {
                    "type": "integer",
                    "description": "(Optional) The ID of the task to be deleted."
                },
                "task_name": {
                    "type": "string",
                    "description": "(Optional) The title or name of the task to be deleted."
                }
            },
            "anyOf": [
                {"required": ["task_id"]},
                {"required": ["task_name"]}
            ]
        }
    }
}
