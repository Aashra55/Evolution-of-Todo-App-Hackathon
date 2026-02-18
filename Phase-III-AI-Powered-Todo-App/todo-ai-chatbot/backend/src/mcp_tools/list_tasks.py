# backend/src/mcp_tools/list_tasks.py
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from src.models.task import Task

def list_tasks(session: Session, user_id: int, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Lists todo tasks for a user, optionally filtering by completion status.
    """
    try:
        query = select(Task).where(Task.user_id == user_id)
        if completed is not None:
            query = query.where(Task.completed == completed)
        
        tasks = session.exec(query).all()
        
        task_list = [{"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for task in tasks]
        
        status_message = "All tasks listed."
        if completed is True:
            status_message = "Completed tasks listed."
        elif completed is False:
            status_message = "Pending tasks listed."

        return {"status": "success", "message": status_message, "tasks": task_list}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": f"Failed to list tasks: {e}"}

# This dictionary defines the schema for the list_tasks tool,
# which can be used by the OpenAI Agent to understand how to call this function.
list_tasks_tool_schema = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "Lists todo tasks for a specific user, optionally filtering by completion status.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user whose tasks are to be listed. This is automatically provided - you should NOT ask the user for it or include it in your tool calls."
                },
                "completed": {
                    "type": "boolean",
                    "description": "(Optional) Filter tasks by their completion status. True for completed, False for pending. If omitted, lists all tasks."
                }
            },
            "required": []  # user_id is automatically provided, don't require it from AI
        }
    }
}
