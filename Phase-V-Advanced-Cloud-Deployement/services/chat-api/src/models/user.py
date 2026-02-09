from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    notificationPreferences = Column(JSON, nullable=True) # Storing preferences as JSON
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship("Task", back_populates="user") # Assuming Task model is defined and accessible

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', email='{self.email}')>"