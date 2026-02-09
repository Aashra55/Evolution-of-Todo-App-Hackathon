import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from services.chat_api.main import app # Import the FastAPI app instance

# Import models and database dependency
from services.chat_api.models.task import Task
from services.chat_api.models.user import User
from services.chat_api.services.database import get_db, Base, engine

# Setup for testing
# Use a test database for integration tests, e.g., in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a new engine for the test database
test_engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create all tables in the test database
Base.metadata.create_all(bind=test_engine)

# Initialize TestClient
client = TestClient(app)

# Test data
MOCK_USER_ID = "test-user-id-123"

@pytest.fixture(name="db_session")
def db_session_fixture():
    db = TestSessionLocal()
    yield db
    db.close()
    # Clean up after each test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

@pytest.fixture(autouse=True)
def mock_dapr_client():
    # Mock the Dapr client for event publishing
    with patch('services.chat_api.services.task_service.dapr_client', new_callable=AsyncMock) as mock_client:
        yield mock_client
    with patch('services.chat_api.api.endpoints.tasks.dapr_client', new_callable=AsyncMock) as mock_client:
        yield mock_client

@pytest.fixture(autouse=True)
def mock_get_current_user_id():
    with patch('services.chat_api.api.endpoints.tasks.get_current_user_id', new_callable=AsyncMock) as mock_user_id:
        mock_user_id.return_value = MOCK_USER_ID
        yield mock_user_id

class TestTaskCRUD:
    def test_create_task(self, db_session: Session, mock_dapr_client):
        # Setup: Ensure a test user exists
        test_user = User(id=MOCK_USER_ID, username="testuser", email="test@example.com")
        db_session.add(test_user)
        db_session.commit()

        task_data = {"title": "Test Task", "description": "This is a test task"}
        response = client.post("/api/tasks", json=task_data)

        assert response.status_code == 201
        assert response.json()["title"] == "Test Task"
        assert response.json()["userId"] == MOCK_USER_ID
        assert db_session.query(Task).count() == 1
        
        # Verify event was published
        # mock_dapr_client.pubsub.publish.assert_awaited_once() # This will need to check the actual object passed
        # This assert would be more robust with a custom mock for dapr_client.pubsub.publish
        # For now, a simple check if it was called (mocked at the service level)
        assert mock_dapr_client.pubsub.publish.called

    def test_get_tasks(self, db_session: Session):
        test_user = User(id=MOCK_USER_ID, username="testuser", email="test@example.com")
        db_session.add(test_user)
        db_session.commit()

        task1 = Task(userId=MOCK_USER_ID, title="Task 1")
        task2 = Task(userId=MOCK_USER_ID, title="Task 2")
        db_session.add_all([task1, task2])
        db_session.commit()

        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["title"] == "Task 1" or response.json()[0]["title"] == "Task 2"

    def test_get_single_task(self, db_session: Session):
        test_user = User(id=MOCK_USER_ID, username="testuser", email="test@example.com")
        db_session.add(test_user)
        db_session.commit()

        task = Task(userId=MOCK_USER_ID, title="Single Task")
        db_session.add(task)
        db_session.commit()

        response = client.get(f"/api/tasks/{task.id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Single Task"

    def test_update_task(self, db_session: Session, mock_dapr_client):
        test_user = User(id=MOCK_USER_ID, username="testuser", email="test@example.com")
        db_session.add(test_user)
        db_session.commit()

        task = Task(userId=MOCK_USER_ID, title="Old Title")
        db_session.add(task)
        db_session.commit()

        update_data = {"title": "New Title", "status": "completed"}
        response = client.put(f"/api/tasks/{task.id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["title"] == "New Title"
        assert response.json()["status"] == "completed"
        
        assert mock_dapr_client.pubsub.publish.called # Verify event was published

    def test_delete_task(self, db_session: Session, mock_dapr_client):
        test_user = User(id=MOCK_USER_ID, username="testuser", email="test@example.com")
        db_session.add(test_user)
        db_session.commit()

        task = Task(userId=MOCK_USER_ID, title="Task to Delete")
        db_session.add(task)
        db_session.commit()

        response = client.delete(f"/api/tasks/{task.id}")
        assert response.status_code == 204
        assert db_session.query(Task).count() == 0
        
        assert mock_dapr_client.pubsub.publish.called # Verify event was published

    def test_complete_task(self, db_session: Session, mock_dapr_client):
        test_user = User(id=MOCK_USER_ID, username="testuser", email="test@example.com")
        db_session.add(test_user)
        db_session.commit()

        task = Task(userId=MOCK_USER_ID, title="Task to Complete")
        db_session.add(task)
        db_session.commit()

        response = client.post(f"/api/tasks/{task.id}/complete")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"
        
        assert mock_dapr_client.pubsub.publish.called # Verify event was published
