from dapr.clients import DaprClient
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

# Assuming conversation state is managed via Dapr State Store
# This service will provide methods to interact with Dapr for state management.

# Initialize Dapr client (can be passed via dependency injection or accessed globally)
# For this example, we'll use a mock client similar to task_service.py for demonstration
# In a real application, this would be a properly initialized DaprClient instance.

class MockDaprClient:
    def __init__(self):
        self.state = self.MockState()

    class MockState:
        def __init__(self):
            self.store = {} # In-memory store for mock

        async def get(self, store_name, key):
            print(f"MockDaprClient: Getting state for key '{key}' from store '{store_name}'")
            value = self.store.get(key)
            return json.dumps(value) if value else None

        async def set(self, store_name, key, value):
            print(f"MockDaprClient: Setting state for key '{key}' in store '{store_name}' with value: {value}")
            self.store[key] = json.loads(value)
            await asyncio.sleep(0.01) # Simulate async operation

dapr_client = MockDaprClient()

async def get_conversation_state(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves conversation state for a given session ID from Dapr State Store.
    """
    state_json = await dapr_client.state.get(store_name="conversationstate", key=session_id)
    if state_json:
        return json.loads(state_json)
    return None

async def set_conversation_state(session_id: str, state: Dict[str, Any]):
    """
    Saves conversation state for a given session ID to Dapr State Store.
    """
    await dapr_client.state.set(store_name="conversationstate", key=session_id, value=json.dumps(state))

async def update_conversation_context(session_id: str, new_context: Dict[str, Any]):
    """
    Updates a specific part of the conversation context.
    Fetches current state, merges, and saves back.
    """
    current_state = await get_conversation_state(session_id)
    if current_state is None:
        current_state = {"sessionId": session_id, "context": {}, "lastInteractionTimestamp": datetime.utcnow().isoformat() + "Z"}
    
    # Merge new context, ensure context is a dict
    if "context" not in current_state or not isinstance(current_state["context"], dict):
        current_state["context"] = {}
    current_state["context"].update(new_context)
    current_state["lastInteractionTimestamp"] = datetime.utcnow().isoformat() + "Z"
    
    await set_conversation_state(session_id, current_state)

async def initialize_conversation(session_id: str):
    """
    Initializes a new conversation state if none exists.
    """
    state = await get_conversation_state(session_id)
    if state is None:
        initial_state = {
            "sessionId": session_id,
            "context": {"initial_prompt": "Welcome to Todo AI Chatbot!"},
            "lastInteractionTimestamp": datetime.utcnow().isoformat() + "Z"
        }
        await set_conversation_state(session_id, initial_state)
        return initial_state
    return state

