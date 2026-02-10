# backend/src/mcp_tools/complete_task.py
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from backend.src.models.task import Task

def complete_task(session: Session, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
    """
    Marks a todo task as completed for a user.
    """
    try:
        task = session.exec(select(Task).where(Task.user_id == user_id, Task.id == task_id)).first()
        if not task:
            return {"status": "error", "message": f"Task with ID {task_id} not found for user {user_id}."}
        
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"status": "success", "message": f"Task '{task.title}' marked as completed.", "task_id": str(task.id)}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"Failed to complete task: {e}"}

# This dictionary defines the schema for the complete_task tool,
# which can be used by the OpenAI Agent to understand how to call this function.
complete_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Marks a specific todo task as completed for a user.",
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
                    "description": "The UUID of the task to be marked as completed."
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
