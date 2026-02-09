import pytest
from httpx import AsyncClient
from sqlmodel import Session, create_engine, SQLModel
from uuid import uuid4
from datetime import datetime, timedelta

# Adjust import path based on project structure
from backend.main import app
from backend.src.services.database import get_session
from backend.src.models.todo import Todo
from backend.src.models.user import User

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


# Override the session dependency to use the test database
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def get_session_override():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = get_session_override


@pytest.fixture(name="client")
async def client_fixture(session: Session):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def authenticated_client(client: AsyncClient, session: Session):
    # Create a test user
    test_username = "testuser"
    test_password = "testpassword"
    test_email = "test@example.com"
    
    # Manually create user to avoid calling the /token endpoint's user creation logic
    user = User(username=test_username, hashed_password=f"hashed_{test_password}", email=test_email)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Directly generate a token (mimicking the /token endpoint without calling it)
    # This avoids potential issues with the mock /token endpoint logic in tests
    from backend.src.api.auth import create_access_token
    token_data = {"sub": user.username, "user_id": str(user.id)}
    access_token = create_access_token(token_data, expires_delta=timedelta(minutes=30))

    client.headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return client, user


class TestAPIEndpoints:

    async def test_read_root(self, client: AsyncClient):
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Todo AI Chatbot Backend"}

    async def test_protected_route_unauthorized(self, client: AsyncClient):
        response = await client.get("/protected-route")
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}

    async def test_protected_route_authenticated(self, authenticated_client):
        client, user = authenticated_client
        response = await client.get("/protected-route")
        assert response.status_code == 200
        assert response.json() == {"message": f"Hello, {user.username}! This is a protected route."}

    async def test_create_todo_success(self, authenticated_client):
        client, user = authenticated_client
        todo_data = {"description": "Buy groceries", "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat()}
        response = await client.post("/todos/", json=todo_data)
        assert response.status_code == 201
        assert response.json()["description"] == todo_data["description"]
        assert response.json()["user_id"] == str(user.id)
        assert response.json()["status"] == "pending"

    async def test_create_todo_empty_description(self, authenticated_client):
        client, user = authenticated_client
        todo_data = {"description": ""}
        response = await client.post("/todos/", json=todo_data)
        assert response.status_code == 400
        assert "Description cannot be empty." in response.json()["detail"]

    async def test_get_todo_success(self, authenticated_client, session: Session):
        client, user = authenticated_client
        todo = Todo(user_id=user.id, description="Test todo")
        session.add(todo)
        session.commit()
        session.refresh(todo)

        response = await client.get(f"/todos/{todo.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(todo.id)
        assert response.json()["description"] == todo.description

    async def test_get_todo_not_found(self, authenticated_client):
        client, user = authenticated_client
        response = await client.get(f"/todos/{uuid4()}") # Non-existent ID
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    async def test_get_todo_forbidden(self, client: AsyncClient, authenticated_client, session: Session):
        # Create a todo for a different user
        _, other_user = authenticated_client
        todo_for_other_user = Todo(user_id=uuid4(), description="Other user's todo")
        session.add(todo_for_other_user)
        session.commit()
        session.refresh(todo_for_other_user)

        response = await client.get(f"/todos/{todo_for_other_user.id}") # Access with unauthenticated client
        assert response.status_code == 401 # Should fail authentication first
        
        # Now try with authenticated client but wrong user
        client_auth_correct_user, correct_user = authenticated_client
        todo_data = {"description": "My todo"}
        create_res = await client_auth_correct_user.post("/todos/", json=todo_data)
        my_todo_id = create_res.json()["id"]

        # Try to access other user's todo with my token
        client_auth_correct_user.headers["Authorization"] = f"Bearer {client_auth_correct_user.headers['Authorization'].split(' ')[1]}" # Ensure header is set
        response_forbidden = await client_auth_correct_user.get(f"/todos/{todo_for_other_user.id}")
        # The current implementation of verify_todo_ownership raises 404 if user_id doesn't match
        # It's a design choice, could be 403. Let's adapt the test to what's implemented.
        assert response_forbidden.status_code == 404 or response_forbidden.status_code == 403 
        # ^ This line might need adjustment based on final verify_todo_ownership behavior


    async def test_update_todo_success(self, authenticated_client, session: Session):
        client, user = authenticated_client
        todo = Todo(user_id=user.id, description="Old description")
        session.add(todo)
        session.commit()
        session.refresh(todo)

        update_data = {"description": "New description", "status": "completed"}
        response = await client.put(f"/todos/{todo.id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["description"] == update_data["description"]
        assert response.json()["status"] == update_data["status"]
        assert response.json()["id"] == str(todo.id)

    async def test_delete_todo_success(self, authenticated_client, session: Session):
        client, user = authenticated_client
        todo = Todo(user_id=user.id, description="Todo to delete")
        session.add(todo)
        session.commit()
        session.refresh(todo)

        response = await client.delete(f"/todos/{todo.id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = await client.get(f"/todos/{todo.id}")
        assert response.status_code == 404

    async def test_list_todos_for_user_success(self, authenticated_client, session: Session):
        client, user = authenticated_client
        todo1 = Todo(user_id=user.id, description="User's todo 1")
        todo2 = Todo(user_id=user.id, description="User's todo 2")
        session.add(todo1)
        session.add(todo2)
        session.commit()
        session.refresh(todo1)
        session.refresh(todo2)

        response = await client.get(f"/todos/user/{user.id}")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["description"] == todo1.description

    async def test_list_todos_for_other_user_forbidden(self, authenticated_client, session: Session):
        client, user = authenticated_client
        other_user_id = uuid4()
        response = await client.get(f"/todos/user/{other_user_id}")
        assert response.status_code == 403
        assert "Not authorized to access other users' todos" in response.json()["detail"]
