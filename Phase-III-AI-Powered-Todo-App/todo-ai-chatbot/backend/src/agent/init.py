# backend/src/agent/init.py
import os
from openai import OpenAI
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# This is a placeholder for the OpenAI Agents SDK setup.
# In a full implementation, you would define your tools, agent, and assistant here.

class OpenAIAgentManager:
    def __init__(self):
        # Configure OpenAI client - support both OpenAI and Gemini APIs
        # First try GEMINI_API_KEY, fall back to OPENAI_API_KEY for compatibility
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if gemini_key:
            api_key = gemini_key
            base_url = os.getenv("OPENAI_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
            self.is_gemini = True
        elif openai_key:
            api_key = openai_key
            base_url = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
            self.is_gemini = False
        else:
            raise ValueError(
                "API key not found. Please set either GEMINI_API_KEY or OPENAI_API_KEY environment variable."
            )
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.assistant_id: Optional[str] = None
        self.tools: List[Dict[str, Any]] = []
        self.use_chat_completions_fallback: bool = False  # Flag to use chat completions if assistant init fails

    def register_tool(self, tool_function: callable, tool_schema: Dict[str, Any]):
        """Registers a tool with the agent manager. (Placeholder - actual registration happens with OpenAI API)"""
        # In a real scenario, this would interact with OpenAI's tool definition API
        # print(f"Tool registered with OpenAI Agent: {tool_schema['function']['name']}")
        pass # Actual tool registration will happen when assistant is created/updated

    async def initialize_assistant(self, instructions: str, model: str = None, tool_schemas: Optional[List[Dict[str, Any]]] = None):
        """Initializes or retrieves an OpenAI Assistant."""
        # Gemini API doesn't support Assistants API, so skip initialization
        if self.is_gemini:
            print("Using Gemini API - Assistants API not supported. Skipping assistant initialization.")
            return
        
        # Default to OpenAI model
        if model is None:
            model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        if self.assistant_id:
            print(f"Assistant already initialized with ID: {self.assistant_id}")
            return

        # Create OpenAI Assistant (only works with OpenAI API)
        try:
            assistant = self.client.beta.assistants.create(
                instructions=instructions,
                model=model,
                tools=tool_schemas if tool_schemas else []
            )
            self.assistant_id = assistant.id
            self.use_chat_completions_fallback = False
            print(f"Initializing assistant with ID: {self.assistant_id}")
        except Exception as e:
            print(f"Warning: Failed to initialize assistant: {e}")
            print("Continuing without assistant initialization. Will use chat completions API as fallback.")
            self.use_chat_completions_fallback = True


    async def process_message(self, user_id: str, conversation_id: str, message_content: str, available_tools: Optional[List[Dict[str, Any]]] = None) -> str:
        """Processes a user message using the OpenAI Assistant or Gemini API."""
        # If using Gemini, use chat completions API instead of Assistants API
        if self.is_gemini:
            print(f"Processing message for user {user_id} in conversation {conversation_id}: {message_content}")
            try:
                response = self.client.chat.completions.create(
                    model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
                    messages=[{"role": "user", "content": message_content}]
                )
                if response and response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        print(f"Gemini response received: {content[:100]}...")
                        return content
                    else:
                        return "I received your message but got an empty response. Please try again."
                else:
                    return "I received your message but couldn't process it. Please try again."
            except Exception as e:
                error_msg = str(e)
                print(f"Gemini API error: {error_msg}")
                # Check if it's an authentication error
                if "401" in error_msg or "invalid" in error_msg.lower() or "api key" in error_msg.lower():
                    return "I'm having trouble connecting to the AI service. Please check your API key configuration. For now, I can help you with task management commands like 'add task', 'list tasks', 'complete task', etc."
                # Return a helpful error message
                return f"I encountered an error while processing your message: {error_msg}. Please try again or use specific task commands like 'add task <title>' or 'list tasks'."
        
        # OpenAI Assistants API flow
        # If assistant initialization failed, fall back to chat completions
        if not self.assistant_id or self.use_chat_completions_fallback:
            print(f"Using chat completions fallback for user {user_id} in conversation {conversation_id}: {message_content}")
            try:
                model = os.getenv("OPENAI_MODEL", "gpt-4o")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message_content}]
                )
                if response and response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        print(f"OpenAI chat completions response received: {content[:100]}...")
                        return content
                    else:
                        return "I received your message but got an empty response. Please try again."
                else:
                    return "I received your message but couldn't process it. Please try again."
            except Exception as e:
                error_msg = str(e)
                print(f"OpenAI API error: {error_msg}")
                # Check if it's an authentication error
                if "401" in error_msg or "invalid" in error_msg.lower() or "api key" in error_msg.lower():
                    return "I'm having trouble connecting to the AI service. Please check your API key configuration. For now, I can help you with task management commands like 'add task', 'list tasks', 'complete task', etc."
                # Return a helpful error message
                return f"I encountered an error while processing your message: {error_msg}. Please try again or use specific task commands like 'add task <title>' or 'list tasks'."

        print(f"Processing message for user {user_id} in conversation {conversation_id}: {message_content}")
        thread = self.client.beta.threads.create(messages=[{"role": "user", "content": message_content}])
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
            tools=available_tools if available_tools else [] # Pass available tools dynamically
        )
        # Await run completion and return response
        import time

        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1) # Wait for 1 second
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            # Find the last assistant message
            for message in messages.data[::-1]: # Reverse to get the latest messages first
                if message.role == 'assistant':
                    # Assuming the response is in the first content block of type text
                    for content_block in message.content:
                        if content_block.type == 'text':
                            return content_block.text.value
            return "No AI response found."
        else:
            return f"Run did not complete successfully. Status: {run.status}"

# Initialize the manager (will be used as a dependency in FastAPI)
openai_agent_manager = OpenAIAgentManager()

async def get_openai_agent_manager():
    """Dependency for FastAPI to get the OpenAI agent manager."""
    return openai_agent_manager
