from fastapi import APIRouter, Depends, HTTPException, status
import uvicorn
import os
from dapr.clients import DaprClient
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import asyncio

# Import structured logging setup
from services.chat_api.src.config.logging import setup_logging
import logging

# Set up logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Import SQLAlchemy models and database session
from services.chat_api.models.user import User # Assuming User model is in user.py
from services.chat_api.models.task import Task # Assuming Task model is in task.py
from services.chat_api.services.database import get_db # Import DB session dependency
# Import Pydantic models for request/response validation
from pydantic import BaseModel, Field

# Import Dapr client and service functions
from dapr.clients import DaprClient
# Import actual service functions, now with DB logic integrated
from services.chat_api.services.task_service import publish_task_event, publish_task_update_event, create_task_in_db, update_task_in_db, delete_task_from_db, get_task_from_db, get_all_tasks_for_user
from services.chat_api.services.conversation_state_service import get_conversation_state, set_conversation_state, update_conversation_context, initialize_conversation


# --- Dapr Client Initialization ---
# Initialize Dapr client. Assumes Dapr sidecar is running and accessible.
try:
    dapr_client = DaprClient()
    logger.info("Dapr client initialized successfully.")
except Exception as e:
    logger.warning(f"Could not initialize Dapr client. Running with mock client. Error: {e}")
    # Define a mock Dapr client if initialization fails, to allow service to run
    class MockDaprClient:
        def __init__(self):
            self.pubsub = self.MockPubSub()
        class MockPubSub:
            async def publish(self, pubsub_name, topic_name, data):
                logger.info(f"MockDaprClient: Publishing to topic '{topic_name}' on pubsub '{pubsub_name}' with data: {data[:100]}...")
                await asyncio.sleep(0.01)
    dapr_client = MockDaprClient()


# --- Pydantic Schemas for Request/Response Validation ---
class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    tags: Optional[List[str]] = None
    dueDate: Optional[datetime] = None
    reminderSettings: Optional[Dict[str, Any]] = None 
    recurrencePattern: Optional[Dict[str, Any]] = None 

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    dueDate: Optional[datetime] = None
    reminderSettings: Optional[Dict[str, Any]] = None
    recurrencePattern: Optional[dict] = None

class ReminderSettingsInput(BaseModel):
    remindAt: datetime
    channel: str = "chat"

class RecurrencePatternInput(BaseModel):
    type: str
    interval: Optional[int] = None
    daysOfWeek: Optional[List[str]] = None
    dayOfMonth: Optional[int] = None
    endDate: Optional[datetime] = None

class ChatMessage(BaseModel):
    message: str
    sessionId: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    parsedIntent: Optional[dict] = None
    suggestedActions: Optional[List[str]] = None

# --- Router Definition ---
router = APIRouter()

# --- API Endpoints ---

@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "createdAt",
    sort_order: Optional[str] = "desc",
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id) 
):
    logger.info(f"Fetching tasks for user {user_id}", extra={
        "filters": {"status": status, "priority": priority, "tags": tags, "search": search, 
                    "sort_by": sort_by, "sort_order": sort_order, "limit": limit, "offset": offset}
    })
    
    # Use TaskQueryService to build the query
    query_service = TaskQueryService(db=db)
    tasks_query = query_service.filter_tasks(
        user_id=user_id,
        status=status,
        priority=priority,
        tags=tags,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    paginated_tasks = tasks_query.limit(limit).offset(offset).all()
    return paginated_tasks

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(task_input: CreateTaskRequest, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task_data = task_input.dict() 
    task_data["userId"] = user_id
    
    new_task = await create_task_in_db(db=db, task_data=task_data, user_id=user_id) # Use actual DB creation function
    
    # Publish event - convert SQLAlchemy object to dict if necessary
    task_dict = new_task.__dict__
    task_dict.pop('_sa_instance_state', None) 
    
    await publish_task_event("TaskCreated", task_dict, user_id)
    
    return new_task

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = await get_task_from_db(db=db, task_id=task_id) # Use actual DB retrieval
    if not task or task.userId != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update_input: UpdateTaskRequest, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = await get_task_from_db(db=db, task_id=task_id) # Use actual DB retrieval
    if not task or task.userId != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = update_input.dict(exclude_unset=True)
    
    await update_task_in_db(db=db, task_id=task_id, update_data=update_data) # Use actual DB update
    
    # Publish event
    await publish_task_update_event(task_id, update_data, user_id)
    
    # Fetch the updated task to return it
    updated_task = await get_task_from_db(db=db, task_id=task_id) # Use actual DB retrieval
    return updated_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    success = await delete_task_from_db(db=db, task_id=task_id) # Use actual DB deletion
    if success:
        event_payload = {
            "eventType": "TaskDeleted",
            "sourceService": "chat-api",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "userId": user_id,
            "payload": {"taskId": task_id},
            "correlationId": str(uuid.uuid4())
        }
        await dapr_client.pubsub.publish(
            pubsub_name="pubsub",
            topic_name="task-events",
            data=json.dumps(event_payload)
        )
        logger.info(f"Published event: TaskDeleted for task {task_id}")
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@router.post("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task or task.userId != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    task.status = "completed"
    task.updatedAt = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    
    await publish_task_update_event(task_id, {"status": "completed"}, user_id)
    
    return task

@router.post("/chat")
async def process_chat_message_endpoint(chat_message: ChatMessage):
    # This endpoint might need access to db session and user_id if chat logic involves tasks
    # For now, it calls the existing process_chat_message function which uses mocks.
    # It should be refactored to use actual service functions and DB access.
    response = await process_chat_message(chat_message.message, chat_message.sessionId)
    return ChatResponse(**response)

@router.post("/reminders")
async def schedule_reminder_endpoint(reminder_request: Dict[str, Any], user_id: str = Depends(get_current_user_id)):
    task_id = reminder_request.get("taskId")
    remind_at_str = reminder_request.get("remindAt")
    channel = reminder_request.get("channel", "chat")

    if not task_id or not remind_at_str:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="taskId and remindAt are required")

    try:
        remind_at = datetime.fromisoformat(remind_at_str.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid datetime format for remindAt")

    # Check if task exists (using actual DB query)
    db = Depends(get_db) # Obtain DB session
    task = db.query(Task).filter(Task.id == task_id).first() 
    if not task or task.userId != user_id: # Simplified check, actual auth needed
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    await schedule_reminder(task_id, remind_at, channel, user_id) # Assuming schedule_reminder publishes event
    return {"message": "Reminder scheduled successfully"}, status.HTTP_202_ACCEPTED

@router.post("/recurring-tasks")
async def define_recurring_task_endpoint(recurring_task_request: Dict[str, Any], user_id: str = Depends(get_current_user_id)):
    title = recurring_task_request.get("title")
    description = recurring_task_request.get("description")
    priority = recurring_task_request.get("priority", "medium")
    tags = recurring_task_request.get("tags")
    dueDate = recurring_task_request.get("dueDate")
    recurrence_pattern = recurring_task_request.get("recurrencePattern")

    if not title or not recurrence_pattern:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title and recurrencePattern are required")

    task_data = {
        "title": title,
        "description": description,
        "priority": priority,
        "tags": tags,
        "dueDate": dueDate,
        "recurrencePattern": recurrence_pattern,
        "userId": user_id
    }
    
    result = await define_recurring_task(task_data, user_id)
    return result, status.HTTP_201_CREATED