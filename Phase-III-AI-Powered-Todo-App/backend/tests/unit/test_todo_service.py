from uuid import UUID, uuid4
from datetime import datetime, timedelta
import pytest
from unittest.mock import MagicMock

from backend.src.models.todo import Todo
from backend.src.services.todo_service import TodoService, TodoNotFoundError


@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def todo_service(mock_session):
    return TodoService(session=mock_session)

@pytest.fixture
def test_user_id():
    return uuid4()

@pytest.fixture
def sample_todo(test_user_id):
    return Todo(
        id=uuid4(),
        user_id=test_user_id,
        description="Buy groceries",
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=1)
    )

class TestTodoService:

    async def test_create_todo_success(self, todo_service, mock_session, test_user_id):
        description = "New test todo"
        due_date = datetime.utcnow() + timedelta(days=2)
        
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda x: None # Mock refresh behavior

        todo = todo_service.create_todo(test_user_id, description, due_date)
        
        assert todo.user_id == test_user_id
        assert todo.description == description
        assert todo.due_date == due_date
        assert todo.status == "pending"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(todo)

    async def test_create_todo_empty_description(self, todo_service, test_user_id):
        with pytest.raises(ValueError, match="Description cannot be empty."):
            todo_service.create_todo(test_user_id, "")

    async def test_create_todo_past_due_date(self, todo_service, test_user_id):
        past_date = datetime.utcnow() - timedelta(days=1)
        with pytest.raises(ValueError, match="Due date must be in the future."):
            todo_service.create_todo(test_user_id, "Description", past_date)

    async def test_get_todo_success(self, todo_service, mock_session, sample_todo):
        mock_session.get.return_value = sample_todo

        retrieved_todo = todo_service.get_todo(sample_todo.user_id, sample_todo.id)
        assert retrieved_todo == sample_todo
        mock_session.get.assert_called_once_with(Todo, sample_todo.id)

    async def test_get_todo_not_found(self, todo_service, mock_session, test_user_id):
        mock_session.get.return_value = None
        with pytest.raises(TodoNotFoundError):
            todo_service.get_todo(test_user_id, uuid4())

    async def test_get_todo_wrong_user(self, todo_service, mock_session, sample_todo):
        mock_session.get.return_value = sample_todo
        with pytest.raises(TodoNotFoundError):
            todo_service.get_todo(uuid4(), sample_todo.id) # Different user ID

    async def test_get_todos_by_user_success(self, todo_service, mock_session, sample_todo, test_user_id):
        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = [sample_todo]
        mock_session.exec.return_value = mock_exec_result

        todos = todo_service.get_todos_by_user(test_user_id)
        assert todos == [sample_todo]
        mock_session.exec.assert_called_once() # Further assert on select statement can be added

    async def test_update_todo_success(self, todo_service, mock_session, sample_todo):
        mock_session.get.return_value = sample_todo
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda x: None

        new_description = "Updated groceries"
        updated_todo = todo_service.update_todo(sample_todo.user_id, sample_todo.id, new_description=new_description)
        
        assert updated_todo.description == new_description
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(updated_todo)

    async def test_update_todo_invalid_status(self, todo_service, mock_session, sample_todo):
        mock_session.get.return_value = sample_todo
        with pytest.raises(ValueError, match="Invalid status: invalid_status."):
            todo_service.update_todo(sample_todo.user_id, sample_todo.id, new_status="invalid_status")

    async def test_delete_todo_success(self, todo_service, mock_session, sample_todo):
        mock_session.get.return_value = sample_todo
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        todo_service.delete_todo(sample_todo.user_id, sample_todo.id)
        mock_session.delete.assert_called_once_with(sample_todo)
        mock_session.commit.assert_called_once()

    async def test_delete_todo_not_found(self, todo_service, mock_session, test_user_id):
        mock_session.get.return_value = None
        with pytest.raises(TodoNotFoundError):
            todo_service.delete_todo(test_user_id, uuid4())
