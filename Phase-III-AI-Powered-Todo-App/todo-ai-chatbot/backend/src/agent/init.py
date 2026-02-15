# backend/src/agent/init.py
import os
import abc
from dotenv import load_dotenv
import google.generativeai as genai
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
    """Agent manager for Google Gemini."""
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest"),
        )
    
    def get_client(self) -> Any:
        return self.model

    async def process_chat_message(
        self, 
        user_id: str, 
        conversation_id: str, 
        message_content: str, 
        system_prompt: str,
        tools: List[Dict[str, Any]],
        tool_schemas: List[Dict[str, Any]]
    ) -> str:
        # Gemini uses the tools parameter directly in generate_content
        chat_model = genai.GenerativeModel(
            model_name=os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest"),
            system_instruction=system_prompt,
            tools=tool_schemas # Pass schemas here
        )
        
        # Start a chat session (or retrieve existing one based on conversation_id)
        chat = chat_model.start_chat()
        
        try:
            # Send message to Gemini
            response = chat.send_message(message_content)
            
            # Check for function calls
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        # Logic to handle function call will be in TodoAgent
                        return response.text # Return the raw response for the agent to process
                        
            # If no function call, return the text response
            return response.text

        except Exception as e:
            error_msg = str(e)
            print(f"Gemini API error: {error_msg}")
            if "api_key" in error_msg.lower():
                # Provide a cleaner error message without command suggestions
                return "I'm having trouble connecting to the AI service. Please check your API key configuration."
            return f"I encountered an error while processing your message: {error_msg}"


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
            if "401" in error_msg or "invalid" in error_msg.lower() or "api key" in error_msg.lower():
                 # Provide a cleaner error message without command suggestions
                return "I'm having trouble connecting to the AI service. Please check your API key configuration."
            return f"I encountered an error while processing your message: {error_msg}"

def get_agent_manager() -> AbstractAgentManager:
    """
    Factory function to get the appropriate agent manager based on environment variables.
    Prioritizes Gemini if GEMINI_API_KEY is set.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if gemini_key:
        print("Initializing Gemini Agent Manager.")
        return GeminiAgentManager(api_key=gemini_key)
    elif openai_key:
        print("Initializing OpenAI Agent Manager.")
        return OpenAIAgentManager(api_key=openai_key)
    else:
        # This will be caught on startup by FastAPI
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
