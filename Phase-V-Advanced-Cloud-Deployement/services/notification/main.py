from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
import os
from dapr.clients import DaprClient
import json
from typing import Dict, Any
from datetime import datetime

# Import structured logging setup
from services.notification.src.config.logging import setup_logging
import logging

# Set up logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Import Dapr client and notification service logic
from services.notification.services.notification_sender import send_notification

app = FastAPI()

# Initialize Dapr client
# In a real application, DaprClient() would be properly managed.
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
                logger.info(f"MockDaprClient: Publishing to topic '{topic_name}'")
                await asyncio.sleep(0.01)
    dapr_client = MockDaprClient()


# Dapr Pub/Sub subscription handler
@app.post('/dapr/subscribe')
async def subscribe_handler():
    return [
        {
            "pubsubname": "pubsub", # Dapr component name for Pub/Sub
            "topic": "reminders",   # Topic to subscribe to
            "route": "/events/reminder" # Route for Dapr to send messages to
        }
    ]

# Handler for messages received on the 'reminders' topic
@app.post('/events/reminder')
async def handle_reminder_event(event_data: Dict[str, Any]):
    event_type = event_data.get("eventType")
    logger.info(f"Received task event from Dapr Pub/Sub: {event_type}", extra={"event_data": event_data})
    
    try:
        # Extract necessary data from the event payload
        task_id = event_data.get("payload", {}).get("taskId")
        remind_at_str = event_data.get("payload", {}).get("remindAt")
        channel = event_data.get("payload", {}).get("channel", "chat")
        user_id = event_data.get("userId")

        if not task_id or not remind_at_str:
            raise ValueError("Missing taskId or remindAt in event payload")

        remind_at = datetime.fromisoformat(remind_at_str.replace('Z', '+00:00'))

        # Call the core notification logic
        await send_notification(task_id=task_id, remind_at=remind_at, channel=channel, user_id=user_id)
        
        # Acknowledge the message (Dapr handles ack based on successful HTTP response)
        return {"message": "Reminder processed and notification sent conceptually."}
    except Exception as e:
        logger.error(f"Error processing reminder event for task {task_id}: {e}", exc_info=True)
        # Return an error status for Dapr to potentially retry
        raise HTTPException(status_code=500, detail=f"Failed to process reminder: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001)) # Use a different port than other services
    logger.info(f"Starting Notification Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)