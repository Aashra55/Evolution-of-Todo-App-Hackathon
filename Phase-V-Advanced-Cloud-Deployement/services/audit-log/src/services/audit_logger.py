import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
import uuid
import logging

# Mock Dapr Client for local development/testing
class MockDaprClient:
    def __init__(self):
        self.pubsub = self.MockPubSub()

    class MockPubSub:
        async def publish(self, pubsub_name, topic_name, data):
            logger.info(f"MockDaprClient: Publishing to topic '{topic_name}' on pubsub '{pubsub_name}' with data: {data[:100]}...")
            await asyncio.sleep(0.01) # Simulate async operation

dapr_client = MockDaprClient()

# --- Mock Audit Log Storage ---
# In a real application, this would interact with a database, logging system,
# or object storage to persist audit records.
MOCK_AUDIT_LOG_DB = []

async def log_event(event_data: Dict[str, Any]):
    """
    Simulates persisting an audit log entry.
    """
    log_entry = {
        "logId": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "receivedEvent": event_data # Store the original event data
    }
    MOCK_AUDIT_LOG_DB.append(log_entry)
    logger.info(f"Audit Log: Event logged - {event_data.get('eventType')} from {event_data.get('sourceService')}")
    
    # Simulate saving to storage
    await asyncio.sleep(0.05)