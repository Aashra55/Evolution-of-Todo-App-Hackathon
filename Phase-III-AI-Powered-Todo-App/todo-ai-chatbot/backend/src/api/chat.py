# backend/src/api/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional

from src.auth import get_current_active_user
from src.agent.agent_logic import get_todo_agent, TodoAgent
from src.config.database import get_session
from src.models.user import User
from src.models.conversation import Conversation
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None # Make conversation_id optional

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    todo_agent: TodoAgent = Depends(get_todo_agent),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that processes user messages using the TodoAgent.
    """
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation_db = session.exec(
                select(Conversation).where(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == current_user.id
                )
            ).first()
        else:
            conversation_db = None

        if not conversation_db:
            conversation_db = Conversation(user_id=current_user.id)
            session.add(conversation_db)
            session.commit()
            session.refresh(conversation_db)
        
        # Process the message using TodoAgent
        print(f"Processing chat message: user_id={current_user.id}, conversation_id={conversation_db.id}, message={request.message}")
        agent_response = await todo_agent.process_chat_message(
            user_id=current_user.id,
            conversation_id=conversation_db.id, # Pass integer ID
            message_content=request.message
        )
        
        print(f"Agent response received: {agent_response[:200] if agent_response else 'None'}...")
        
        # Commit the session to save any database changes made by tools
        session.commit()
        
        if not agent_response:
            agent_response = "I received your message but couldn't generate a response. Please try again."
        
        return {
            "user_id": current_user.id,
            "conversation_id": conversation_db.id,
            "response": agent_response
        }
    except Exception as e:
        # Rollback on error
        session.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in chat endpoint: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
