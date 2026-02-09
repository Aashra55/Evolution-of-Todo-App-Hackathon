from fastapi import Depends
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime
import json # ADDED IMPORT

from sqlmodel import Session, Field, SQLModel, create_engine, select

from .database import get_session
from ..models.conversation import Conversation # ADDED IMPORT


class ConversationService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_or_create_conversation(self, user_id: UUID, conversation_id: Optional[UUID] = None) -> Conversation:
        with self.session:
            if conversation_id:
                conversation = self.session.get(Conversation, conversation_id)
                if conversation and conversation.user_id == user_id:
                    return conversation
            
            # If no conversation_id or not found/owned, create a new one
            new_conversation = Conversation(user_id=user_id, history="[]")
            self.session.add(new_conversation)
            self.session.commit()
            self.session.refresh(new_conversation)
            return new_conversation

    def update_conversation_history(self, conversation_id: UUID, new_entry: Dict[str, Any]) -> Conversation:
        with self.session:
            conversation = self.session.get(Conversation, conversation_id)
            if not conversation:
                raise ValueError(f"Conversation with ID {conversation_id} not found.")
            
            history_list = json.loads(conversation.history)
            history_list.append(new_entry)
            conversation.history = json.dumps(history_list)
            conversation.updated_at = datetime.utcnow()
            
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
            return conversation

    def get_conversation_history(self, conversation_id: UUID) -> List[Dict[str, Any]]:
        with self.session:
            conversation = self.session.get(Conversation, conversation_id)
            if not conversation:
                return []
            return json.loads(conversation.history)
