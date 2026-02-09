from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import os
from dapr.clients import DaprClient
import json
import asyncio
from typing import Dict, Any, List

# Import structured logging setup
from services.real_time_sync.src.config.logging import setup_logging
import logging

# Set up logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Import services
from services.real_time_sync.services.websocket_manager import manager
from services.real_time_sync.services.message_formatter import format_dapr_event_to_websocket_message

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
            "topic": "task-updates",
            "route": "/events/task-update" # Route for Dapr to send task update events
        }
    ]

# Handler for task events
@app.post('/events/task')
async def handle_task_event(event_data: Dict[str, Any]):
    event_type = event_data.get("eventType")
    logger.info(f"Received task event from Dapr Pub/Sub: {event_type}", extra={"event_data": event_data})
    
    try:
        # Format the Dapr event into a WebSocket message
        ws_message = await format_dapr_event_to_websocket_message(event_data)
        
        # Broadcast the message to all connected clients
        await manager.broadcast(ws_message)
        
        return {"message": f"Task event {event_type} received and broadcasted."}
    except Exception as e:
        logger.error(f"Error processing task event {event_type}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process task event: {e}")

# Handler for task update events
@app.post('/events/task-update')
async def handle_task_update_event(event_data: Dict[str, Any]):
    event_type = event_data.get("eventType") # Should be TaskUpdated
    logger.info(f"Received task update event from Dapr Pub/Sub: {event_type}", extra={"event_data": event_data})
    
    try:
        # Format the Dapr event into a WebSocket message
        ws_message = await format_dapr_event_to_websocket_message(event_data)

        # Broadcast the message to all connected clients
        await manager.broadcast(ws_message)
        
        return {"message": f"Task update event {event_type} received and broadcasted."}
    except Exception as e:
        logger.error(f"Error processing task update event {event_type}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process task update event: {e}")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, or handle specific client messages (e.g., heartbeats, subscriptions)
            data = await websocket.receive_text() # Or receive_json() if clients send JSON
            logger.info(f"Received message from client {websocket.client}: {data}")
            # Example: client sends "ping", respond with "pong"
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"WebSocket connection disconnected from {websocket.client}")
    except Exception as e:
        logger.error(f"Error in WebSocket connection with {websocket.client}: {e}", exc_info=True)
        manager.disconnect(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8003)) # Use a different port
    logger.info(f"Starting Real-time Sync Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
