from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import asyncio
import json

# Import SQLAlchemy models and database session
from services.chat_api.models.user import User # Assuming User model is in user.py
from services.chat_api.models.task import Task # Assuming Task model is in task.py
from services.chat_api.services.database import get_db # Import DB session dependency
from pydantic import BaseModel, Field # Import BaseModel for request/response validation

# Import Dapr client and event publishing functions
from dapr.clients import DaprClient
from services.chat_api.services.task_service import publish_task_event, publish_task_update_event, create_task_in_db, update_task_in_db, delete_task_from_db, get_task_from_db, get_all_tasks_for_user # Import actual service functions
from services.chat_api.services.conversation_state_service import get_conversation_state, set_conversation_state, update_conversation_context, initialize_conversation # Import conversation state service

# --- Mock Dapr Client Initialization ---
# This mock client assumes Dapr is running and accessible.
# In a real application, DaprClient() would be properly initialized and managed.
class MockDaprClient:
    def __init__(self):
        self.pubsub = self.MockPubSub()
        self.state = self.MockState()

    class MockPubSub:
        async def publish(self, pubsub_name, topic_name, data):
            print(f"MockDaprClient: Publishing to topic '{topic_name}' on pubsub '{pubsub_name}' with data: {data[:100]}...")
            await asyncio.sleep(0.01)

    class MockState:
        def __init__(self):
            self.store = {}
        async def get(self, store_name, key):
            value = self.store.get(key)
            print(f"MockDaprClient: Getting state for key '{key}' from '{store_name}': {'Found' if value else 'Not Found'}")
            return json.dumps(value) if value else None
        async def set(self, store_name, key, value):
            print(f"MockDaprClient: Setting state for key '{key}' in '{store_name}'")
            self.store[key] = json.loads(value)
            await asyncio.sleep(0.01)

dapr_client = MockDaprClient() # Global instance for services to use

# --- Pydantic Schemas for Request/Response Validation ---
# These align with OpenAPI specs and data models.

class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    tags: Optional[List[str]] = None
    dueDate: Optional[datetime] = None
    # Using Dict for reminderSettings and recurrencePattern for simplicity, can be Pydantic models
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

# Schemas for reminder and recurrence input structures (can be Pydantic models)
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
    logger.info(f"Fetching tasks for user {user_id}", extra={"filters": {"status": status, "priority": priority, "tags": tags, "search": search, "sort_by": sort_by, "sort_order": sort_order, "limit": limit, "offset": offset}})
    
    query = db.query(Task).filter(Task.userId == user_id)

    if status: query = query.filter(Task.status == status)
    if priority: query = query.filter(Task.priority == priority)
    if tags:
        # This assumes tags are stored in a JSONB column for PostgreSQL.
        # Adjust if using a different storage or format for tags.
        # Example for PostgreSQL JSONB: query = query.filter(Task.tags.contains(tags))
        pass # Placeholder for tag filtering logic
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
        query = query.order_by(Task.createdAt.desc())

    paginated_tasks = query.limit(limit).offset(offset).all()
    return paginated_tasks

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(task_input: CreateTaskRequest, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task_data = task_input.dict() 
    task_data["userId"] = user_id
    
    new_task = await create_task_in_db(task_data) # Use actual DB creation function (currently mock)
    
    # Publish event - convert SQLAlchemy object to dict if necessary
    task_dict = new_task.__dict__
    task_dict.pop('_sa_instance_state', None) 
    
    await publish_task_event("TaskCreated", task_dict, user_id)
    
    return new_task

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task or task.userId != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update_input: UpdateTaskRequest, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task or task.userId != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = update_input.dict(exclude_unset=True)
    
    # Apply updates to task object, ensuring JSON compatibility for complex types
    for key, value in update_data.items():
        if value is not None:
            if key in ["reminderSettings", "recurrencePattern"] and isinstance(value, dict):
                value = json.dumps(value) # Ensure JSON serializable
            setattr(task, key, value)
    task.updatedAt = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    
    # Publish event
    await publish_task_update_event(task_id, update_data, user_id)
    
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task or task.userId != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(task)
    await db.commit()
    
    # Publish event
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

@router.post("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task or task.userId != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    task.status = "completed"
    task.updatedAt = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    
    # Publish event
    await publish_task_update_event(task_id, {"status": "completed"}, user_id)
    
    return task

@router.post("/chat")
async def process_chat_message_endpoint(chat_message: ChatMessage):
    # This endpoint might need access to db session and user_id if chat logic involves tasks
    # For now, it calls the existing mock process_chat_message
    response = await process_chat_message(chat_message.message, chat_message.sessionId)
    return ChatResponse(**response)

@router.post("/reminders")
async def schedule_reminder_endpoint(reminder_request: dict, user_id: str = Depends(get_current_user_id)):
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
async def define_recurring_task_endpoint(recurring_task_request: dict, user_id: str = Depends(get_current_user_id)):
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

# --- Helper functions for mock services (replace with actual imports and logic) ---
# NOTE: These mock functions are used because the actual DB and Dapr interactions
# are handled elsewhere or are conceptual at this stage. In a real implementation,
# these would be replaced by actual service calls using SQLAlchemy and DaprClient.

async def publish_task_event(event_type: str, task_data: dict, user_id: str = None):
    logger.info(f"Publishing task event: {event_type}", extra={"task_id": task_data.get('id'), "user_id": user_id, "event_type": event_type})
    # In a real app, this would use DaprClient.pubsub.publish
    # Using the mock client defined globally
    await dapr_client.pubsub.publish(
        pubsub_name="pubsub",
        topic_name="task-events",
        data=json.dumps({"eventType": event_type, **task_data, "userId": user_id, "timestamp": datetime.utcnow().isoformat() + "Z"})
    )

async def publish_task_update_event(task_id: str, changes: dict, user_id: str = None):
    logger.info(f"Publishing task update event for task {task_id}", extra={"changes": changes, "user_id": user_id})
    # In a real app, this would use DaprClient.pubsub.publish
    await dapr_client.pubsub.publish(
        pubsub_name="pubsub",
        topic_name="task-updates",
        data=json.dumps({"eventType": "TaskUpdated", "taskId": task_id, "changes": changes, "userId": user_id, "timestamp": datetime.utcnow().isoformat() + "Z"})
    )

async def create_task_in_db(task_data): # Mock DB operation
    task_id = str(uuid.uuid4())
    # Ensure reminderSettings and recurrencePattern are JSON serializable if they are dicts
    if 'reminderSettings' in task_data and isinstance(task_data['reminderSettings'], dict):
        task_data['reminderSettings'] = json.dumps(task_data['reminderSettings'])
    if 'recurrencePattern' in task_data and isinstance(task_data['recurrencePattern'], dict):
        task_data['recurrencePattern'] = json.dumps(task_data['recurrencePattern'])
    
    new_task = Task(id=task_id, **task_data) # Using SQLAlchemy Task model
    db = SessionLocal() # Get a DB session
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    logger.info(f"DB: Created task with ID {task_id}")
    return new_task

async def update_task_in_db(task_id, update_data): # Mock DB operation
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        for key, value in update_data.items():
            if value is not None:
                if key in ['reminderSettings', 'recurrencePattern'] and isinstance(value, dict):
                    value = json.dumps(value) # Ensure JSON serializable
                setattr(task, key, value)
        task.updatedAt = datetime.utcnow()
        db.commit()
        db.refresh(task)
        logger.info(f"DB: Updated task {task_id}")
    return task

async def delete_task_from_db(task_id): # Mock DB operation
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        logger.info(f"DB: Deleted task {task_id}")
        return True
    return False

async def get_task_from_db(task_id): # Mock DB operation
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    logger.info(f"DB: Getting task {task_id}")
    return task

async def get_all_tasks_for_user(db: Session, user_id: str): # Mock DB operation
    logger.info(f"DB: Getting all tasks for user {user_id}")
    return db.query(Task).filter(Task.userId == user_id).all()

async def schedule_reminder(task_id, remind_at, channel, user_id): # Mock service call
    logger.info(f"Scheduling reminder for task {task_id} at {remind_at} via {channel}")
    # Simulate publishing an event
    event_payload = {
        "eventType": "ReminderScheduled",
        "sourceService": "chat-api",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "userId": user_id,
        "payload": {"taskId": task_id, "remindAt": remind_at.isoformat() + "Z", "channel": channel, "status": "scheduled"},
        "correlationId": str(uuid.uuid4())
    }
    await dapr_client.pubsub.publish(
        pubsub_name="pubsub",
        topic_name="reminders",
        data=json.dumps(event_payload)
    )
    print(f"Published event: ReminderScheduled for task {task_id}")


async def define_recurring_task(task_data, user_id): # Mock service call
    logger.info(f"Defining recurring task: {task_data.get('title')} with pattern {task_data.get('recurrencePattern')}")
    # Simulate creating a base task for the recurring definition and returning confirmation
    # In reality, this might involve complex logic and storing the pattern.
    return {"message": "Recurring task definition processed", "taskId": str(uuid.uuid4()), "title": task_data['title']}

async def process_chat_message(message: str, session_id: str = None): # Mock service call
    logger.info(f"Processing chat message: '{message}' for session {session_id}")
    # Placeholder for NLP and intent processing
    # This function should delegate to actual service functions (create_task, update_task, etc.)
    # For now, it uses mock DB functions and mock publish functions.
    if "create task" in message.lower():
        task_data = {"title": message.replace("create task", "").strip(), "userId": await get_current_user_id()}
        new_task = await create_task_in_db(task_data)
        await publish_task_event("TaskCreated", new_task.__dict__, await get_current_user_id())
        return {"response": f"Task '{new_task.title}' created with ID {new_task.id}."}
    elif "complete task" in message.lower():
        task_id_to_complete = message.lower().replace("complete task", "").strip()
        if task_id_to_complete:
            await update_task_in_db(task_id_to_complete, {"status": "completed"})
            await publish_task_update_event(task_id_to_complete, {"status": "completed"}, await get_current_user_id())
            return {"response": f"Task {task_id_to_complete} marked as complete."}
        else:
            return {"response": "Please specify which task to complete."}
    else:
        return {"response": "I understood your message, but cannot perform an action yet. Try 'create task [your task title]' or 'complete task [task_id]'."}

# --- Main application setup ---
# This ensures that when the script is run directly, it starts the FastAPI app.
# When run via Dapr, the Dapr sidecar manages the app's lifecycle.

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting Chat API Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
