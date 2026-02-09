from sqlalchemy.orm import Session
from sqlalchemy import func, cast, JSON
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Assuming Task model is accessible
from services.chat_api.models.task import Task # Actual import

class TaskQueryService:
    def __init__(self, db: Session):
        self.db = db

    def filter_tasks(self, user_id: str, status: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, search: Optional[str] = None, sort_by: str = "createdAt", sort_order: str = "desc") -> List[Task]:
        
        query = self.db.query(Task).filter(Task.userId == user_id)

        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if tags:
            # This assumes tags are stored in a JSONB column for PostgreSQL.
            # For other databases, this might need adjustment.
            # Example for PostgreSQL JSONB:
            query = query.filter(Task.tags.contains(tags)) 
            # If tags were a simple string column with comma-separated values, it would be:
            # query = query.filter(Task.tags.ilike(f"%{','.join(tags)}%")) # Very basic, not robust
        if search:
            query = query.filter(
                (Task.title.ilike(f"%{search}%")) | 
                (Task.description.ilike(f"%{search}%"))
            )

        # Sorting
        if sort_by in ["createdAt", "dueDate", "priority"]:
            sort_column = getattr(Task, sort_by)
            query = query.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())
        else:
            query = query.order_by(Task.createdAt.desc()) # Default sort

        return query # Return the query object for pagination

# Example usage within an endpoint (conceptual)
# async def get_tasks_endpoint(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id), ... filters ...):
#     query_service = TaskQueryService(db=db)
#     tasks_query = query_service.filter_tasks(user_id=user_id, status=status, priority=priority, tags=tags, search=search, sort_by=sort_by, sort_order=sort_order)
#     paginated_tasks = tasks_query.limit(limit).offset(offset).all()
#     return paginated_tasks

