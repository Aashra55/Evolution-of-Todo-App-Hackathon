# backend/src/mcp_tools/delete_task.py
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from backend.src.models.task import Task

def delete_task(session: Session, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
    """
    Deletes a todo task for a user.
    """
    try:
        task = session.exec(select(Task).where(Task.user_id == user_id, Task.id == task_id)).first()
        if not task:
            return {"status": "error", "message": f"Task with ID {task_id} not found for user {user_id}."}
        
        session.delete(task)
        session.commit()
        return {"status": "success", "message": f"Task '{task.title}' deleted successfully.", "task_id": str(task.id)}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"Failed to delete task: {e}"}

# This dictionary defines the schema for the delete_task tool,
# which can be used by the OpenAI Agent to understand how to call this function.
delete_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Deletes a specific todo task for a user.",
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
                    "description": "The UUID of the task to be deleted."
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
