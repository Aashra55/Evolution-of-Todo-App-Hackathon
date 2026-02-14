# backend/src/api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from sqlmodel import Session

from src.agent.agent_logic import get_todo_agent, TodoAgent
from src.config.database import get_session

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    todo_agent: TodoAgent = Depends(get_todo_agent),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that processes user messages using the TodoAgent.
    """
    try:
        # Convert string IDs to UUIDs
        try:
            user_uuid = UUID(user_id)
            conversation_uuid = UUID(request.conversation_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
        
        # Process the message using TodoAgent
        print(f"Processing chat message: user_id={user_id}, conversation_id={request.conversation_id}, message={request.message}")
        agent_response = await todo_agent.process_chat_message(
            user_id=user_uuid,
            conversation_id=conversation_uuid,
            message_content=request.message
        )
        
        print(f"Agent response received: {agent_response[:200] if agent_response else 'None'}...")
        
        # Commit the session to save any database changes made by tools
        session.commit()
        
        if not agent_response:
            agent_response = "I received your message but couldn't generate a response. Please try again."
        
        return {
            "user_id": user_id,
            "conversation_id": request.conversation_id,
            "response": agent_response
        }
    except Exception as e:
        # Rollback on error
        session.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in chat endpoint: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
