# src/models/task.py

class Task:
    def __init__(self, description: str, identifier: int):
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Task description cannot be empty.")
        if not isinstance(identifier, int) or identifier <= 0:
            raise ValueError("Task identifier must be a positive integer.")

        self.description = description.strip()
        self.status = "active"  # Default status
        self.identifier = identifier

    def mark_complete(self):
        self.status = "complete"

    def mark_incomplete(self):
        self.status = "active"

    def __repr__(self):
        return (f"Task(id={self.identifier}, "
                f"description='{self.description}', "
                f"status='{self.status}')")

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return (self.identifier == other.identifier and
                self.description == other.description and
                self.status == other.status)

    def to_dict(self):
        return {
            "id": self.identifier,
            "description": self.description,
            "status": self.status
        }