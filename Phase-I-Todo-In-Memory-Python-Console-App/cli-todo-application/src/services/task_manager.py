# src/services/task_manager.py

from src.models.task import Task


class TaskManager:
    def __init__(self):
        self._tasks = []  # Internal list to store Task objects
        self._next_id = 1  # Simple ID generator

    def add_task(self, description: str) -> Task:
        task = Task(description=description, identifier=self._next_id)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        # Return a copy to prevent external modification
        return list(self._tasks)

    def get_task_by_id(self, task_id: int) -> Task | None:
        for task in self._tasks:
            if task.identifier == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_description: str) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            if not isinstance(new_description, str) or not new_description.strip():
                raise ValueError("New task description cannot be empty.")
            task.description = new_description.strip()
            return True
        return False

    def mark_task_complete(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_complete()
            return True
        return False

    def mark_task_incomplete(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_incomplete()
            return True
        return False

    def remove_task(self, task_id: int) -> bool:
        initial_len = len(self._tasks)
        self._tasks = [
            task for task in self._tasks if task.identifier != task_id
        ]
        # True if a task was removed
        return len(self._tasks) < initial_len