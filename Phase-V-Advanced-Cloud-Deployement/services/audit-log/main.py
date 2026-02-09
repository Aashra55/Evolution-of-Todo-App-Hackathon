from fastapi import FastAPI, HTTPException, status
import uvicorn
import os
from dapr.clients import DaprClient
import json
from typing import Dict, Any
import asyncio

# Import structured logging setup
from services.audit_log.src.config.logging import setup_logging
import logging

# Set up logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Import Dapr client for Pub/Sub
try:
    dapr_client = DaprClient()
    logger.info("Dapr client initialized.")
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

# Import audit logging service logic
from services.audit_log.services.audit_logger import log_event

app = FastAPI()

# Dapr Pub/Sub subscription handler
@app.post('/dapr/subscribe')
async def subscribe_handler():
    return [
        {
            "pubsubname": "pubsub",
            "topic": "task-events",
            "route": "/events/task" # Route for Dapr to send task events
        },
        {
            "pubsubname": "pubsub",
            "topic": "reminders",
            "route": "/events/reminder" # Route for Dapr to send reminder events
        },
        {
            "pubsubname": "pubsub",
            "topic": "task-updates",
            "route": "/events/task-update" # Route for Dapr to send task update events
        }
    ]

@app.post('/events/task')
async def handle_task_event(event_data: Dict[str, Any]):
    event_type = event_data.get("eventType")
    logger.info(f"Received task event: {event_type}", extra={"event_payload": event_data})
    await log_event(event_data) # Log the event using the service logic
    return {"message": f"Task event {event_type} received and logged."}

@app.post('/events/reminder')
async def handle_reminder_event(event_data: Dict[str, Any]):
    event_type = event_data.get("eventType")
    logger.info(f"Received reminder event: {event_type}", extra={"event_payload": event_data})
    await log_event(event_data) # Log the event
    return {"message": f"Reminder event {event_type} received and logged."}

@app.post('/events/task-update')
async def handle_task_update_event(event_data: Dict[str, Any]):
    event_type = event_data.get("eventType")
    logger.info(f"Received task update event: {event_type}", extra={"event_payload": event_data})
    await log_event(event_data) # Log the event
    return {"message": f"Task update event {event_type} received and logged."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8002)) # Use a different port
    logger.info(f"Starting Audit Log Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)