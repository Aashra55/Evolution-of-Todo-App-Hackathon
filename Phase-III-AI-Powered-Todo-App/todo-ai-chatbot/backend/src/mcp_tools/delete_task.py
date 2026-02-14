# backend/src/mcp_tools/delete_task.py
from typing import Dict, Any, Union
from uuid import UUID
from sqlmodel import Session, select
from src.models.task import Task

def delete_task(session: Session, user_id: UUID, task_id: Union[UUID, str, int]) -> Dict[str, Any]:
    """
    Deletes a todo task for a user.
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
