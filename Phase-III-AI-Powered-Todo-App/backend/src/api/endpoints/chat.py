from typing import Annotated, Optional
from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import httpx # New: For making HTTP calls to AI Agent
import os # New: For AI_AGENT_URL

from src.models.user import User
from src.services.conversation_service import ConversationService
from src.api.auth import get_authenticated_user
# from ai_agent.src.agents.main_agent import initialize_agent # REMOVED


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(get_authenticated_user)] # Chat endpoint is protected
)


class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: UUID

# REMOVED: ai_agent = initialize_agent()

# New: Configuration for AI Agent endpoint
AI_AGENT_URL = os.getenv("AI_AGENT_URL", "http://localhost:8001/chat") # Assuming AI Agent will expose /chat on 8001


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    chat_message: ChatMessage,
    current_user: Annotated[User, Depends(get_authenticated_user)],
    conversation_service: Annotated[ConversationService, Depends(ConversationService)]
):
    if not current_user or not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required for chat."
        )

    conversation = conversation_service.get_or_create_conversation(current_user.id, chat_message.conversation_id)

    conversation_service.update_conversation_history(
        conversation.id,
        {"role": "user", "content": chat_message.message, "timestamp": datetime.utcnow().isoformat()}
    )

    # New: Mock AI Agent interaction or call a separate AI Agent service
    try:
        # In a full setup, the AI Agent would be a separate microservice
        # Here, we simulate calling it via HTTP.
        # This requires the AI Agent to also expose a /chat endpoint
        # For this quick fix, I will mock the response.
        
        # This is where an HTTP call to the AI Agent would be:
        # async with httpx.AsyncClient() as client:
        #     agent_api_response = await client.post(AI_AGENT_URL, json={
        #         "user_message": chat_message.message,
        #         "conversation_id": str(conversation.id),
        #         "current_user_id": str(current_user.id)
        #     })
        #     agent_api_response.raise_for_status()
        #     agent_response = agent_api_response.json()

        # Mocked AI Agent response for now to allow backend startup
        if "create todo" in chat_message.message.lower():
            mock_reply = f"Okay, I'll create a todo for '{chat_message.message.replace('create todo', '').strip()}'. (Mocked AI Agent)"
        elif "list todos" in chat_message.message.lower():
            mock_reply = "Here are your todos: (Mocked AI Agent response, actual todos not fetched)."
        else:
            mock_reply = f"I received your message: '{chat_message.message}'. (Mocked AI Agent response)."

        agent_response = {"reply": mock_reply}

    except Exception as e:
        print(f"Error communicating with AI Agent: {e}")
        agent_response = {"reply": f"Error: Could not get response from AI Agent ({e})."}
    
    conversation_service.update_conversation_history(
        conversation.id,
        {"role": "agent", "content": agent_response.get("reply", ""), "timestamp": datetime.utcnow().isoformat()}
    )

    return ChatResponse(reply=agent_response.get("reply", "An error occurred."), conversation_id=conversation.id)
