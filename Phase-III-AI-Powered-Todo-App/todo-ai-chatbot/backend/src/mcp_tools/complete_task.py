# backend/src/mcp_tools/complete_task.py
from typing import Dict, Any, Union
from sqlmodel import Session, select
from src.models.task import Task

def complete_task(session: Session, user_id: int, task_id: int) -> Dict[str, Any]:
    """
    Marks a todo task as completed for a user.
    """
    try:
        task_id_int = task_id
        
        task = session.exec(select(Task).where(Task.user_id == user_id, Task.id == task_id_int)).first()
        if not task:
            return {"status": "error", "message": f"Task with ID {task_id} not found for user {user_id}."}
        
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"status": "success", "message": f"Task '{task.title}' marked as completed.", "task_id": task.id}
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
                    "type": "integer",
                    "description": "The ID of the user who owns the task. This is automatically provided - you should NOT ask the user for it or include it in your tool calls."
                },
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to be marked as completed."
                }
            },
            "required": ["task_id"]
        }
    }
}
