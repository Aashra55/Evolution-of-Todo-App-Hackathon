# backend/src/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlmodel import Session

from src.config.database import get_session
from src.mcp_tools.list_tasks import list_tasks

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

