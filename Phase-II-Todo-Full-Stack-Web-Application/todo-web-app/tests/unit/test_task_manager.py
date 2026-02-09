# tests/unit/test_task_manager.py

import pytest
from src.models.task import Task
from src.services.task_manager import TaskManager

def test_task_creation():
    task = Task("Buy groceries", 1)
    assert task.description == "Buy groceries"
    assert task.identifier == 1
    assert task.status == "active"

def test_task_creation_empty_description_raises_error():
    with pytest.raises(ValueError, match="Task description cannot be empty."):
        Task("", 1)
    with pytest.raises(ValueError, match="Task description cannot be empty."):
        Task("   ", 1)

def test_task_creation_invalid_identifier_raises_error():
    with pytest.raises(ValueError, match="Task identifier must be a positive integer."):
        Task("Test", 0)
    with pytest.raises(ValueError, match="Task identifier must be a positive integer."):
        Task("Test", -1)

def test_add_task():
    manager = TaskManager()
    task1 = manager.add_task("First task")
    assert task1.description == "First task"
    assert task1.identifier == 1
    assert len(manager.get_all_tasks()) == 1

    task2 = manager.add_task("Second task")
    assert task2.description == "Second task"
    assert task2.identifier == 2
    assert len(manager.get_all_tasks()) == 2

def test_get_all_tasks():
    manager = TaskManager()
    assert manager.get_all_tasks() == []

    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    all_tasks = manager.get_all_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0] == task1
    assert all_tasks[1] == task2

    # Ensure returning a copy
    all_tasks_copy = manager.get_all_tasks()
    all_tasks_copy.append(Task("Extra task", 99))
    assert len(manager.get_all_tasks()) == 2 # Manager's internal list should be unchanged

def test_mark_task_complete():
    manager = TaskManager()
    task1 = manager.add_task("Task to complete")
    task2 = manager.add_task("Another task")

    # Mark existing task as complete
    assert manager.mark_task_complete(task1.identifier) is True
    assert task1.status == "complete"
    assert task2.status == "active" # Ensure other tasks are not affected

    # Try to mark non-existent task
    assert manager.mark_task_complete(999) is False

def test_remove_task():
    manager = TaskManager()
    task1 = manager.add_task("Task to remove")
    task2 = manager.add_task("Task to keep")

    # Remove existing task
    assert manager.remove_task(task1.identifier) is True
    assert len(manager.get_all_tasks()) == 1
    assert manager.get_all_tasks()[0] == task2

    # Try to remove non-existent task
    assert manager.remove_task(999) is False
    assert len(manager.get_all_tasks()) == 1 # List should remain unchanged

def test_update_task():
    manager = TaskManager()
    task = manager.add_task("Original description")

    # Update existing task
    assert manager.update_task(task.identifier, "Updated description") is True
    updated_task = manager.get_task_by_id(task.identifier)
    assert updated_task.description == "Updated description"

    # Try to update non-existent task
    assert manager.update_task(999, "Non-existent update") is False

    # Try to update with empty description
    with pytest.raises(ValueError, match="New task description cannot be empty."):
        manager.update_task(task.identifier, "")
    with pytest.raises(ValueError, match="New task description cannot be empty."):
        manager.update_task(task.identifier, "   ")

def test_mark_task_incomplete():
    manager = TaskManager()
    task = manager.add_task("Task to mark incomplete")
    manager.mark_task_complete(task.identifier) # Mark it complete first

    # Mark existing task as incomplete
    assert manager.mark_task_incomplete(task.identifier) is True
    assert task.status == "active"

    # Try to mark non-existent task as incomplete
    assert manager.mark_task_incomplete(999) is False