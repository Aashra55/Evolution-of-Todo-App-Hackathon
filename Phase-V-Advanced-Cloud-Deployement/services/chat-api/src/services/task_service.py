from dapr.clients import DaprClient
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

# Import SQLAlchemy models and database session
from sqlalchemy.orm import Session
from sqlalchemy import func, cast # Import necessary SQLAlchemy components
# Import Base from models.user as it's the assumed source for Base definition
from services.chat_api.models.user import Base # Import Base from user model
from services.chat_api.models.task import Task # Import Task model
from services.chat_api.services.database import get_db # Import DB session dependency

import asyncio # Required for mock sleep in Dapr client mock

# Import structured logging setup
from services.chat_api.src.config.logging import setup_logging
import logging

# Set up logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# --- Dapr Client Initialization ---
# Initialize Dapr client. This assumes Dapr sidecar is running and accessible.
# For local development without sidecar, a mock or testing client might be used.
try:
    dapr_client = DaprClient()
    logger.info("Dapr client initialized successfully.")
except Exception as e:
    logger.warning(f"Could not initialize Dapr client. Running with mock client. Error: {e}")
    # Define a mock Dapr client if initialization fails, to allow service to run
    class MockDaprClient:
        def __init__(self):
            self.pubsub = self.MockPubSub()
            self.state = self.MockState()

        class MockPubSub:
            async def publish(self, pubsub_name, topic_name, data):
                logger.info(f"MockDaprClient: Publishing to topic '{topic_name}' on pubsub '{pubsub_name}' with data: {data[:100]}...")
                await asyncio.sleep(0.01)

        class MockState:
            def __init__(self):
                self.store = {}
            async def get(self, store_name, key):
                value = self.store.get(key)
                logger.debug(f"MockDaprClient: Getting state for key '{key}' from '{store_name}': {'Found' if value else 'Not Found'}")
                return json.dumps(value) if value else None
            async def set(self, store_name, key, value):
                logger.debug(f"MockDaprClient: Setting state for key '{key}' in '{store_name}'")
                self.store[key] = json.loads(value)
                await asyncio.sleep(0.01)
    dapr_client = MockDaprClient()


# --- Task Service Logic ---

async def create_task_in_db(db: Session, task_data: dict, user_id: str):
    """Creates a new task in the database using SQLAlchemy."""
    task_id = str(uuid.uuid4())
    # Ensure complex types are JSON serialized if stored as JSON in DB
    if 'reminderSettings' in task_data and isinstance(task_data['reminderSettings'], dict):
        task_data['reminderSettings'] = json.dumps(task_data['reminderSettings'])
    if 'recurrencePattern' in task_data and isinstance(task_data['recurrencePattern'], dict):
        task_data['recurrencePattern'] = json.dumps(task_data['recurrencePattern'])
    
    new_task = Task(id=task_id, userId=user_id, **task_data)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    logger.info(f"DB: Created task with ID {task_id}")
    return new_task

async def update_task_in_db(db: Session, task_id: str, update_data: dict):
    """Updates an existing task in the database using SQLAlchemy."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        for key, value in update_data.items():
            if value is not None:
                if key in ['reminderSettings', 'recurrencePattern'] and isinstance(value, dict):
                    value = json.dumps(value)
                setattr(task, key, value)
        task.updatedAt = datetime.utcnow()
        db.commit()
        db.refresh(task)
        logger.info(f"DB: Updated task {task_id}")
    return task

async def delete_task_from_db(db: Session, task_id: str):
    """Deletes a task from the database."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        logger.info(f"DB: Deleted task {task_id}")
        return True
    return False

async def get_task_from_db(db: Session, task_id: str):
    """Retrieves a single task from the database."""
    task = db.query(Task).filter(Task.id == task_id).first()
    logger.debug(f"DB: Getting task {task_id}")
    return task

async def get_all_tasks_for_user(db: Session, user_id: str):
    """Retrieves all tasks for a specific user."""
    logger.info(f"DB: Getting all tasks for user {user_id}")
    return db.query(Task).filter(Task.userId == user_id).all()


async def publish_task_event(event_type: str, task_data: dict, user_id: str = None):
    """
    Publishes a task event using Dapr Pub/Sub.
    """
    event_payload = {
        "eventType": event_type,
        "sourceService": "chat-api",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "userId": user_id,
        "payload": task_data,
        "correlationId": str(uuid.uuid4()) # Example correlation ID
    }
    await dapr_client.pubsub.publish(
        pubsub_name="pubsub", # Dapr component name for Pub/Sub
        topic_name="task-events",
        data=json.dumps(event_payload)
    )
    logger.info(f"Published event: {event_type} for task {task_data.get('id', 'N/A')}")

async def publish_task_update_event(task_id: str, changes: dict, user_id: str = None):
    """
    Publishes a task update event using Dapr Pub/Sub.
    """
    event_payload = {
        "eventType": "TaskUpdated",
        "sourceService": "chat-api",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "userId": user_id,
        "payload": {
            "taskId": task_id,
            "changes": changes,
            "fullTask": None # Optionally include full task data if needed
        },
        "correlationId": str(uuid.uuid4())
    }
    await dapr_client.pubsub.publish(
        pubsub_name="pubsub",
        topic_name="task-updates",
        data=json.dumps(event_payload)
    )
    logger.info(f"Published event: TaskUpdated for task {task_id}")

# Note: The functions create_task, update_task, delete_task, schedule_reminder, define_recurring_task, process_chat_message
# from the previous version were mock wrappers. They are now replaced by direct calls to DB functions
# and Dapr publishing functions. These service functions are intended to be called by the API endpoints.
# Their mock behavior is removed in favor of actual (or conceptually real) DB/Dapr interactions.
