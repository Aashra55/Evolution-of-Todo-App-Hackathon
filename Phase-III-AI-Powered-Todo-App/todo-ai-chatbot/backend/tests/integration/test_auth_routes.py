import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from src.main import app
from src.config.database import get_session
from src.models.user import User

# Override the DATABASE_URL for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session
    
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_register_user(client: TestClient):
    response = client.post(
        "/api/register",
        json={"username": "testuser", "password": "testpassword", "email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_for_access_token(client: TestClient):
    # First, register a user
    client.post(
        "/api/register",
        json={"username": "testuser", "password": "testpassword", "email": "test@example.com"}
    )
    
    # Then, attempt to login
    response = client.post(
        "/api/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password(client: TestClient):
    # First, register a user
    client.post(
        "/api/register",
        json={"username": "testuser", "password": "testpassword", "email": "test@example.com"}
    )
    
    # Then, attempt to login with incorrect password
    response = client.post(
        "/api/token",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
