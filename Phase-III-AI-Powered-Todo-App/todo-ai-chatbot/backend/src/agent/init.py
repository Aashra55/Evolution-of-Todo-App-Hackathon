# backend/src/agent/init.py
import os
import abc
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any, Optional

# Load environment variables from .env file
load_dotenv()

class AbstractAgentManager(abc.ABC):
    """Abstract base class for AI agent managers."""
    
    @abc.abstractmethod
    def get_client(self) -> Any:
        """Get the underlying AI client."""
        pass

    @abc.abstractmethod
    async def process_chat_message(
        self, 
        user_id: str, 
        conversation_id: str, 
        message_content: str, 
        system_prompt: str,
        tools: List[Dict[str, Any]],
        tool_schemas: List[Dict[str, Any]]
    ) -> str:
        """Processes a chat message using the configured AI service."""
        pass

class GeminiAgentManager(AbstractAgentManager):
    """Agent manager for Google Gemini using OpenAI-compatible API."""
    def __init__(self, api_key: str):
        # Use OpenAI-compatible API endpoint for Gemini
        # The correct base URL for Gemini OpenAI-compatible API
        # Format: https://generativelanguage.googleapis.com/v1beta/openai/
        base_url = os.getenv("OPENAI_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
        
        print(f"Initializing Gemini client with base_url: {base_url}")
        
        # For Gemini OpenAI-compatible API, pass API key to OpenAI client
        # The client will use it in Authorization: Bearer <key> header
        self.client = OpenAI(
            api_key=api_key, 
            base_url=base_url
        )
        self.api_key = api_key
    
    def get_client(self) -> Any:
        return self.client

    async def process_chat_message(
        self, 
        user_id: str, 
        conversation_id: str, 
        message_content: str, 
        system_prompt: str,
        tools: List[Dict[str, Any]],
        tool_schemas: List[Dict[str, Any]]
    ) -> str:
        # This method is not used directly - TodoAgent handles the actual processing
        # But we keep it for interface compatibility
        try:
            response = self.client.chat.completions.create(
                model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message_content}
                ],
                tools=tool_schemas,
                tool_choice="auto",
            )
            return response.choices[0].message.content or "I received your message but couldn't generate a response."
        except Exception as e:
            error_msg = str(e)
            print(f"Gemini API error: {error_msg}")
            if "api" in error_msg.lower() and "key" in error_msg.lower():
                return "I'm having trouble connecting to the AI service. Please check your API key configuration."
            return "I encountered an error while processing your message. Please try again."


class OpenAIAgentManager(AbstractAgentManager):
    """Agent manager for OpenAI."""
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_API_BASE_URL"))
    
    def get_client(self) -> Any:
        return self.client
    
    async def process_chat_message(
        self, 
        user_id: str, 
        conversation_id: str, 
        message_content: str, 
        system_prompt: str,
        tools: List[Dict[str, Any]],
        tool_schemas: List[Dict[str, Any]] # Note: OpenAI uses 'tools' in the create call
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message_content}
                ],
                tools=tool_schemas,
                tool_choice="auto",
            )
            return response.choices[0].message
        except Exception as e:
            error_msg = str(e)
            print(f"OpenAI API error: {error_msg}")
            if "401" in error_msg or "invalid" in error_msg.lower() or "api" in error_msg.lower() and "key" in error_msg.lower():
                return "I'm having trouble connecting to the AI service. Please check your API key configuration."
            return "I encountered an error while processing your message. Please try again."

def get_agent_manager() -> AbstractAgentManager:
    """
    Factory function to get the appropriate agent manager based on environment variables.
    Prioritizes Gemini if GEMINI_API_KEY is set, or auto-detects Gemini keys (starting with 'AIza').
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    # Priority 1: Explicit GEMINI_API_KEY
    if gemini_key:
        print("Initializing Gemini Agent Manager (from GEMINI_API_KEY).")
        return GeminiAgentManager(api_key=gemini_key)
    
    # Priority 2: Auto-detect Gemini keys in OPENAI_API_KEY (they start with "AIza")
    if openai_key and openai_key.startswith("AIza"):
        print("Detected Gemini API key in OPENAI_API_KEY. Initializing Gemini Agent Manager.")
        return GeminiAgentManager(api_key=openai_key)
    
    # Priority 3: Regular OpenAI key
    if openai_key:
        print("Initializing OpenAI Agent Manager.")
        return OpenAIAgentManager(api_key=openai_key)
    
    # No key found
    raise ValueError("No AI provider key found. Please set either GEMINI_API_KEY or OPENAI_API_KEY.")

# Single instance of the agent manager, determined by the factory.
try:
    agent_manager_instance = get_agent_manager()
except ValueError as e:
    print(f"CRITICAL: {e}")
    agent_manager_instance = None

async def get_current_agent_manager() -> Optional[AbstractAgentManager]:
    """Dependency for FastAPI to get the current agent manager."""
    return agent_manager_instance
