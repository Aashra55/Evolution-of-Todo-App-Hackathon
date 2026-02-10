# backend/tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine
import os

# Import the main FastAPI app and database components
from backend.src.main import app
from backend.src.config.database import create_db_and_tables, get_session
from backend.src.models.task import Task
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message

# Override the DATABASE_URL for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="client")
def client_fixture():
    # Use an in-memory SQLite database for testing
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine) # Create tables for models

    with TestClient(app) as client:
        # Override get_session to use the test database
        def get_test_session():
            with Session(engine) as session:
                yield session
        app.dependency_overrides[get_session] = get_test_session
        yield client
    
    SQLModel.metadata.drop_all(engine) # Clean up after tests
    app.dependency_overrides.clear() # Clear overrides

def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_chat_endpoint_add_task(client: TestClient):
    user_id = uuid4()
    conversation_id = uuid4()
    message = "Add task: Buy groceries"
    
    response = client.post(f"/api/{user_id}/chat", json={"message": message, "conversation_id": str(conversation_id)})
    assert response.status_code == 200
    
    response_json = response.json()
    assert "response" in response_json
    
    # The agent's response is a JSON string
    agent_response = response_json["response"]
    agent_response_parsed = json.loads(agent_response)
    
    assert agent_response_parsed["status"] == "success"
    assert "task_id" in agent_response_parsed
    assert agent_response_parsed["message"] == "Task 'Buy groceries' added successfully."

def test_chat_endpoint_list_tasks(client: TestClient):
    user_id = uuid4()
    conversation_id = uuid4()
    
    # First, add some tasks
    client.post(f"/api/{user_id}/chat", json={"message": "Add task: Task A", "conversation_id": str(conversation_id)})
    client.post(f"/api/{user_id}/chat", json={"message": "Add task: Task B", "conversation_id": str(conversation_id)})

    # Then list tasks
    response = client.post(f"/api/{user_id}/chat", json={"message": "List my tasks", "conversation_id": str(conversation_id)})
    assert response.status_code == 200
    
    response_json = response.json()
    assert "response" in response_json
    
    agent_response = response_json["response"]
    agent_response_parsed = json.loads(agent_response)
    
    assert agent_response_parsed["status"] == "success"
    assert len(agent_response_parsed["tasks"]) == 2
    assert any(task["title"] == "Task A" for task in agent_response_parsed["tasks"])
    assert any(task["title"] == "Task B" for task in agent_response_parsed["tasks"])

def test_chat_endpoint_complete_task(client: TestClient):
    user_id = uuid4()
    conversation_id = uuid4()

    # Add a task
    add_response = client.post(f"/api/{user_id}/chat", json={"message": "Add task: Finish report", "conversation_id": str(conversation_id)})
    add_response_parsed = json.loads(add_response.json()["response"])
    task_id = add_response_parsed["task_id"]

    # Complete the task
    complete_message = f"Complete task with ID: {task_id}"
    complete_response = client.post(f"/api/{user_id}/chat", json={"message": complete_message, "conversation_id": str(conversation_id)})
    assert complete_response.status_code == 200
    
    complete_response_parsed = json.loads(complete_response.json()["response"])
    assert complete_response_parsed["status"] == "success"
    assert "marked as completed" in complete_response_parsed["message"]

    # Verify task is completed by listing
    list_response = client.post(f"/api/{user_id}/chat", json={"message": "List completed tasks", "conversation_id": str(conversation_id)})
    list_response_parsed = json.loads(list_response.json()["response"])
    assert list_response_parsed["status"] == "success"
    assert any(task["id"] == task_id and task["completed"] is True for task in list_response_parsed["tasks"])
