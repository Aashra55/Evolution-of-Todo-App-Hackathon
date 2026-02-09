from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum("pending", "completed", "in_progress", "cancelled"), default="pending")
    priority = Column(Enum("low", "medium", "high", "urgent"), default="medium")
    tags = Column(JSON, nullable=True)
    dueDate = Column(DateTime, nullable=True)
    reminderSettings = Column(JSON, nullable=True) # Added reminder settings
    recurrencePattern = Column(JSON, nullable=True) # Added recurrence pattern
    userId = Column(String, ForeignKey("users.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id='{self.id}', title='{self.title}', status='{self.status}')>"

# Placeholder classes for ReminderSettings and RecurrencePattern if they were separate models,
# but for simplicity, they are often stored as JSONB in PostgreSQL or directly in the Task model.
# If modeled separately, they would be SQLAlchemy models with ForeignKey to Task.id.
# For this task, we assume they might be JSON fields or handled within the main Task model's logic.
