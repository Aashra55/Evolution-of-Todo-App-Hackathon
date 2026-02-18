# backend/src/mcp_tools/delete_task.py
from typing import Dict, Any, Union
from sqlmodel import Session, select
from src.models.task import Task

def delete_task(session: Session, user_id: int, task_id: int) -> Dict[str, Any]:
    """
    Deletes a todo task for a user.
    """
    try:
        task_id_int = task_id
        
        task = session.exec(select(Task).where(Task.user_id == user_id, Task.id == task_id_int)).first()
        if not task:
            return {"status": "error", "message": f"Task with ID {task_id} not found for user {user_id}."}
        
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
        "description": "Deletes a specific todo task for a user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user who owns the task. This is automatically provided - you should NOT ask the user for it or include it in your tool calls."
                },
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to be deleted."
                }
            },
            "required": ["task_id"]
        }
    }
}
