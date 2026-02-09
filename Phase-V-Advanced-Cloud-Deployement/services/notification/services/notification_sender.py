import asyncio
import json
from datetime import datetime
from typing import Dict, Any
import uuid
import logging

# Import structured logging setup
from services.notification.src.config.logging import setup_logging
import logging

# Set up logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Import Dapr client
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
                await asyncio.sleep(0.01) # Simulate async operation
    dapr_client = MockDaprClient()


async def send_notification(task_id: str, remind_at: datetime, channel: str, user_id: str = None):
    """
    Sends a notification to a user via the specified channel.
    This function simulates sending notifications and publishes an event upon completion.
    In a real application, this would integrate with actual notification services.
    """
    message_content = f"Reminder: Task '{task_id}' is due at {remind_at.isoformat()}."
    
    logger.info(f"Sending notification for task {task_id} to user {user_id} via {channel} at {remind_at.isoformat()}.")

    # Simulate sending logic based on channel
    if channel == "email":
        logger.info(f"  -> Simulating sending email to user {user_id}.")
        await asyncio.sleep(0.1) 
    elif channel == "app_notification":
        logger.info(f"  -> Simulating sending app notification to user {user_id}.")
        await asyncio.sleep(0.1)
    elif channel == "chat":
        logger.info(f"  -> Simulating sending chat message to user {user_id}.")
        await asyncio.sleep(0.1)
    else:
        logger.warning(f"Unknown channel '{channel}'. No notification sent.")

    # Publish an event indicating the notification was processed/sent
    notification_event = {
        "eventType": "NotificationSent",
        "sourceService": "notification-service",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "userId": user_id,
        "payload": {
            "taskId": task_id,
            "remindAt": remind_at.isoformat() + "Z",
            "channel": channel,
            "status": "sent" 
        },
        "correlationId": str(uuid.uuid4())
    }
    await dapr_client.pubsub.publish(
        pubsub_name="pubsub",
        topic_name="notifications", # Example topic for notification events
        data=json.dumps(notification_event)
    )
    logger.info(f"Published event: NotificationSent for task {task_id}")