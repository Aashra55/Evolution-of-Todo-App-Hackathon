from fastapi import FastAPI, HTTPException, status
import uvicorn
import os
from dapr.clients import DaprClient
import json
import asyncio # Required for mock sleep

# Import structured logging setup
from services.recurring_task.src.config.logging import setup_logging
import logging

# Set up logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Import service logic
from services.recurring_task.services.recurrence_generator import generate_recurring_tasks_job

app = FastAPI()

# Dapr Pub/Sub subscription for task events
@app.post('/dapr/subscribe')
async def subscribe_handler():
    return [
        {
            "pubsubname": "pubsub",
            "topic": "task-events",
            "route": "/events/task" # Route for Dapr to send messages to
        }
    ]

@app.post('/events/task')
async def task_event_handler(event_data: dict):
    logger.info(f"Received task event: {event_data.get('eventType')}")
    try:
        if event_data.get("eventType") in ["TaskCreated", "TaskUpdated"]:
            logger.info("Task event received, checking for recurring task generation...")
            await generate_recurring_tasks_job() 
        
        return {"message": "Task event received and processed."}
    except Exception as e:
        logger.error(f"Error processing task event: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process task event: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001)) # Use a different port than chat-api
    logger.info(f"Starting Recurring Task Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
