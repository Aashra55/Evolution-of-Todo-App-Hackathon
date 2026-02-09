from typing import Dict, Any
import json
from datetime import datetime

async def format_dapr_event_to_websocket_message(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates a Dapr event payload into a WebSocket message format suitable for clients.
    """
    event_type = event_data.get("eventType")
    timestamp = event_data.get("timestamp", datetime.utcnow().isoformat() + "Z")
    payload = event_data.get("payload")

    ws_message = {
        "type": "UNKNOWN_EVENT",
        "payload": payload,
        "timestamp": timestamp
    }

    if event_type == "TaskCreated":
        ws_message["type"] = "TASK_CREATED"
        # The payload should contain the full task object
        ws_message["payload"] = payload # Assuming payload is already the task object
    elif event_type == "TaskUpdated":
        ws_message["type"] = "TASK_UPDATED"
        # Payload should contain taskId and changes, optionally fullTask
        ws_message["payload"] = payload
    elif event_type == "TaskDeleted":
        ws_message["type"] = "TASK_DELETED"
        # Payload should contain taskId
        ws_message["payload"] = payload
    elif event_type == "RecurringTaskGenerated":
        ws_message["type"] = "TASK_CREATED" # Treat as a new task being created
        ws_message["payload"] = payload # Payload is the generated task object
    elif event_type == "ReminderScheduled":
        ws_message["type"] = "REMINDER_SCHEDULED"
        ws_message["payload"] = payload
    
    # Add other event types as needed

    return ws_message
