from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
import pytest

from main import app
from database import get_session

# Use a test database
TEST_DATABASE_URL = "sqlite:///./test.db"  # Use in-memory for faster tests if preferred "sqlite://"
engine = create_engine(TEST_DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


def get_test_session():
    with Session(engine) as session:
        yield session


@pytest.fixture(name="session")
def session_fixture():
    drop_db_and_tables()  # Ensure clean slate
    create_db_and_tables()
    yield Session(engine)
    drop_db_and_tables()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_user(client: TestClient):
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_create_user_duplicate_email(client: TestClient):
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Email already registered"


def test_login_for_access_token(client: TestClient):
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_for_access_token_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/token",
        data={"username": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Incorrect username or password"
