# backend/src/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlmodel import Session

from src.config.database import get_session
from src.mcp_tools.list_tasks import list_tasks
from src.mcp_tools.complete_task import complete_task
from src.mcp_tools.update_task import update_task

router = APIRouter()

@router.get("/{user_id}/tasks")
async def get_tasks_endpoint(
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    Direct endpoint to get tasks for a user without going through the chat agent.
    """
    try:
        # Convert string ID to UUID
        try:
            user_uuid = UUID(user_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
        
        # Use the list_tasks MCP tool directly
        result = list_tasks(session=session, user_id=user_uuid, completed=None)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message", "Failed to fetch tasks"))
        
        return {
            "status": "success",
            "tasks": result.get("tasks", []),
            "message": result.get("message", "Tasks retrieved successfully")
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in tasks endpoint: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router.patch("/{user_id}/tasks/{task_id}/toggle")
async def toggle_task_endpoint(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status (complete if pending, uncomplete if completed).
    """
    try:
        # Convert string IDs to UUIDs
        try:
            user_uuid = UUID(user_id)
            task_id_int = int(task_id)  # Task ID is integer
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid ID format: {str(e)}")
        
        # First, get the current task to check its status
        from src.models.task import Task
        from sqlmodel import select
        
        user_id_str = str(user_uuid)
        task = session.exec(select(Task).where(Task.user_id == user_id_str, Task.id == task_id_int)).first()
        
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        
        # Toggle the completion status
        new_completed_status = not task.completed
        
        # Use update_task MCP tool to update the task
        result = update_task(
            session=session,
            user_id=user_uuid,
            task_id=task_id_int,
            completed=new_completed_status
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message", "Failed to toggle task"))
        
        return {
            "status": "success",
            "message": result.get("message", "Task status updated successfully"),
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": new_completed_status
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in toggle task endpoint: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Error toggling task: {str(e)}")

