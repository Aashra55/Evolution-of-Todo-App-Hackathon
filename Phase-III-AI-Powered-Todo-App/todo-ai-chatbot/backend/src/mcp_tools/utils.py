# backend/src/mcp_tools/utils.py
from typing import Optional, Union
from sqlmodel import Session, select, col
from src.models.task import Task

def find_task(session: Session, user_id: int, task_id: Optional[int] = None, task_name: Optional[str] = None) -> Optional[Task]:
    """
    Finds a task by ID or name (case-insensitive title match).
    """
    if task_id is not None:
        return session.exec(select(Task).where(Task.user_id == user_id, Task.id == task_id)).first()
    
    if task_name:
        # Try exact match first
        task = session.exec(select(Task).where(
            Task.user_id == user_id, 
            Task.title == task_name
        )).first()
        
        if not task:
            # Try case-insensitive title match
            task = session.exec(select(Task).where(
                Task.user_id == user_id,
                col(Task.title).ilike(f"%{task_name}%")
            )).first()
            
        return task
    
    return None
