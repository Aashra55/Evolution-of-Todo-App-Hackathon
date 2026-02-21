# backend/tests/unit/mcp_tools/test_mcp_tools.py
import pytest
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine
import datetime

# Import the MCP tools and models to be tested
from src.models.task import Task
from src.mcp_tools.add_task import add_task
from src.mcp_tools.list_tasks import list_tasks
from src.mcp_tools.complete_task import complete_task
from src.mcp_tools.delete_task import delete_task
from src.mcp_tools.update_task import update_task


# Use an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine) # Clean up after tests

def test_add_task(session: Session):
    user_id = 1
    title = "Buy groceries"
    description = "Milk, Eggs, Bread"
    
    result = add_task(session, user_id, title, description)
    assert result["status"] == "success"
    assert "task_id" in result
    
    task_in_db = session.get(Task, int(result["task_id"]))
    assert task_in_db is not None
    assert task_in_db.user_id == user_id
    assert task_in_db.title == title
    assert task_in_db.description == description
    assert task_in_db.completed is False

def test_list_tasks(session: Session):
    user_id = 1
    add_task(session, user_id, "Task 1", "Desc 1")
    add_task(session, user_id, "Task 2", "Desc 2")
    
    tasks = list_tasks(session, user_id)
    assert tasks["status"] == "success"
    assert len(tasks["tasks"]) == 2
    assert tasks["tasks"][0]["title"] == "Task 1"

    # Test filtering by completed status
    result_completed = list_tasks(session, user_id, completed=True)
    assert result_completed["status"] == "success"
    assert len(result_completed["tasks"]) == 0

    result_pending = list_tasks(session, user_id, completed=False)
    assert result_pending["status"] == "success"
    assert len(result_pending["tasks"]) == 2

def test_complete_task(session: Session):
    user_id = 1
    add_result = add_task(session, user_id, "Task to complete")
    task_id = int(add_result["task_id"])

    complete_result = complete_task(session, user_id, task_id)
    assert complete_result["status"] == "success"
    assert complete_result["message"] == f"Task 'Task to complete' marked as completed."

    task_in_db = session.get(Task, task_id)
    assert task_in_db.completed is True

def test_delete_task(session: Session):
    user_id = 1
    add_result = add_task(session, user_id, "Task to delete")
    task_id = int(add_result["task_id"])

    delete_result = delete_task(session, user_id, task_id)
    assert delete_result["status"] == "success"
    assert delete_result["message"] == f"Task 'Task to delete' deleted successfully."

    task_in_db = session.get(Task, task_id)
    assert task_in_db is None

def test_update_task(session: Session):
    user_id = 1
    add_result = add_task(session, user_id, "Original Title", "Original Description")
    task_id = int(add_result["task_id"])

    # Update title
    update_result_title = update_task(session, user_id, task_id, title="New Title")
    assert update_result_title["status"] == "success"
    task_in_db_title = session.get(Task, task_id)
    assert task_in_db_title.title == "New Title"
    assert task_in_db_title.description == "Original Description" # Description should be unchanged

    # Update description and completed status
    update_result_desc_comp = update_task(session, user_id, task_id, description="New Description", completed=True)
    assert update_result_desc_comp["status"] == "success"
    task_in_db_desc_comp = session.get(Task, task_id)
    assert task_in_db_desc_comp.title == "New Title" # Title should be unchanged
    assert task_in_db_desc_comp.description == "New Description"
    assert task_in_db_desc_comp.completed is True

    # Test updating non-existent task
    non_existent_id = 999
    error_result = update_task(session, user_id, non_existent_id, title="Non-existent")
    assert error_result["status"] == "error"
    assert "not found" in error_result["message"]
