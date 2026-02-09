from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"WebSocket disconnected: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcasts a JSON message to all active WebSocket connections.
        Handles potential disconnections during broadcast.
        """
        message_json = json.dumps(message) # Convert dict to JSON string
        disconnected_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except WebSocketDisconnect:
                disconnected_connections.append(connection)
            except Exception as e:
                print(f"Error broadcasting to {connection.client}: {e}")
                disconnected_connections.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected_connections:
            self.active_connections.remove(conn)
        
        print(f"Broadcasted message to {len(self.active_connections)} active clients.")

manager = ConnectionManager() # Global instance of connection manager
