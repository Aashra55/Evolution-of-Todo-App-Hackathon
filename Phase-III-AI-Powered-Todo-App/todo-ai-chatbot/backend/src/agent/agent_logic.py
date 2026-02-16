# backend/src/agent/agent_logic.py
import json
import os
from typing import Dict, Any, List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlmodel import Session

from src.agent.init import AbstractAgentManager, get_current_agent_manager, GeminiAgentManager, OpenAIAgentManager
from src.config.database import get_session
from src.mcp_tools.add_task import add_task, add_task_tool_schema
from src.mcp_tools.list_tasks import list_tasks, list_tasks_tool_schema
from src.mcp_tools.complete_task import complete_task, complete_task_tool_schema
from src.mcp_tools.delete_task import delete_task, delete_task_tool_schema
from src.mcp_tools.update_task import update_task, update_task_tool_schema

class TodoAgent:
    def __init__(self, agent_manager: AbstractAgentManager, session: Session):
        self.agent_manager = agent_manager
        self.session = session
        # The tool functions themselves
        self.tool_functions = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task
        }
        # The schemas for the tools, used by the AI
        self.tool_schemas = [
            add_task_tool_schema,
            list_tasks_tool_schema,
            complete_task_tool_schema,
            delete_task_tool_schema,
            update_task_tool_schema
        ]

    async def process_chat_message(self, user_id: UUID, conversation_id: UUID, message_content: str) -> str:
        """
        Processes a chat message using the configured AI, intelligently deciding which tools to use.
        """
        system_prompt = """You are a helpful and friendly AI Todo Chatbot. Your primary role is to assist users in managing their todo lists through natural language conversation. You have access to a set of tools to add, list, update, complete, and delete tasks.

Guidelines:
- Be conversational and use natural language.
- Infer the user's intent and use the available tools to fulfill their requests.
- When a user wants to act on a task (e.g., 'complete the first one'), you may need to first use the `list_tasks` tool to get the task ID.
- Always confirm the successful completion of an action (e.g., "Okay, I've added 'Buy milk' to your list.").
- If an operation fails, explain the reason in a clear and friendly manner.
- Do not return raw JSON to the user. Always provide a text-based, friendly response based on the tool's output."""

        try:
            # Both Gemini and OpenAI use OpenAI-compatible API format
            client = self.agent_manager.get_client()
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_content}
            ]
            
            # Determine model name based on agent type
            if isinstance(self.agent_manager, GeminiAgentManager):
                # Try different Gemini model names - newer models first
                model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # Try newest model first
                # List of fallback models to try (newer to older)
                gemini_models = [
                    model_name,
                    "gemini-2.5-pro",
                    "gemini-2.5-flash",
                    "gemini-2.5-flash-lite",
                    "gemini-2.5-flash-lite-preview",
                    "gemini-2.5-flash-lite-preview-2",
                    "gemini-2.5-flash-lite-preview-3",
                    "gemini-2.5-flash-lite-preview-4",
                    "gemini-2.5-flash-lite-preview-5",
                    "gemini-2.5-flash-lite-preview-6",
                    "gemini-2.5-flash-lite-preview-7",
                    "gemini-2.5-flash-lite-preview-8",
                    "gemini-2.5-flash-lite-preview-9",
                    "gemini-2.5-flash-lite-preview-10",
                    "gemini-2.0-flash",
                    "gemini-1.5-flash-latest",
                    "gemini-1.5-flash",
                    "gemini-1.5-pro-latest",
                    "gemini-1.5-pro",
                    "gemini-pro"
                ]
            else:
                model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
                gemini_models = [model_name]
            
            # Try calling with tools - if model not found, try fallback models
            last_error = None
            response = None
            
            # Try with tools first, if that fails, try without tools
            for try_model in gemini_models:
                try:
                    # First try with tools (function calling)
                    response = client.chat.completions.create(
                        model=try_model,
                        messages=messages,
                        tools=self.tool_schemas,
                        tool_choice="auto",
                    )
                    model_name = try_model  # Update to successful model
                    break
                except Exception as e:
                    last_error = e
                    error_str = str(e)
                    print(f"Error with model {try_model}: {error_str[:200]}")  # Print first 200 chars of error
                    # If it's a model not found error, try next model
                    if "404" in error_str or "not found" in error_str.lower() or "not supported" in error_str.lower():
                        print(f"Model {try_model} not found or doesn't support tools, trying next model...")
                        continue
                    else:
                        # Other errors, raise immediately
                        raise
            
            # If no model worked with tools, try without tools as fallback
            if response is None and isinstance(self.agent_manager, GeminiAgentManager):
                print("Function calling not supported, trying without tools...")
                for try_model in gemini_models:
                    try:
                        response = client.chat.completions.create(
                            model=try_model,
                            messages=messages,
                            # Don't include tools parameter
                        )
                        model_name = try_model
                        print(f"Using model {try_model} without function calling support")
                        # Return simple response since no function calling
                        if response and response.choices and response.choices[0].message.content:
                            return response.choices[0].message.content
                        break
                    except Exception as e:
                        last_error = e
                        error_str = str(e)
                        if "404" in error_str or "not found" in error_str.lower():
                            continue
                        raise
            
            if response is None:
                raise Exception(f"Could not find a valid Gemini model. Last error: {last_error}")
            
            response_message = response.choices[0].message
            
            # Check if AI wants to call tools
            tool_calls = getattr(response_message, 'tool_calls', None)
            if not tool_calls:
                return response_message.content or "I received your message but couldn't generate a response. Please try again."
            
            # Add assistant message with tool calls
            messages.append(response_message)
            
            # Execute all tool calls
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    function_args = {}
                
                # Inject user_id (convert to UUID if needed) and ensure session is first
                if 'user_id' in function_args:
                    # Convert string to UUID if needed
                    if isinstance(function_args['user_id'], str):
                        function_args['user_id'] = UUID(function_args['user_id'])
                else:
                    function_args['user_id'] = user_id
                
                # Get the tool function
                tool_function = self.tool_functions.get(function_name)
                if tool_function:
                    # Execute tool with session as first parameter
                    try:
                        function_response = tool_function(self.session, **function_args)
                    except Exception as e:
                        function_response = {"status": "error", "message": f"Error executing {function_name}: {str(e)}"}
                else:
                    function_response = {"status": "error", "message": f"Unknown tool: {function_name}"}
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(function_response)
                })
            
            # Second call to get final response
            second_response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            
            final_message = second_response.choices[0].message
            return final_message.content or "I processed your request but didn't get a response. Please try again."

        except Exception as e:
            error_msg = str(e)
            print(f"Error processing chat message: {error_msg}")
            
            # Handle specific error types
            error_lower = error_msg.lower()
            
            # API key errors
            if "api" in error_lower and "key" in error_lower:
                return "I'm having trouble connecting to the AI service. Please check your API key configuration."
            
            # Model not found errors
            if "404" in error_msg or "not found" in error_lower or "not supported" in error_lower:
                return "I'm having trouble with the AI model configuration. Please check your API settings."
            
            # Network/connection errors
            if "connection" in error_lower or "timeout" in error_lower or "network" in error_lower:
                return "I'm having trouble connecting to the AI service. Please check your internet connection and try again."
            
            # Generic error
            return "I encountered an error while processing your request. Please try again."

async def get_todo_agent(
    agent_manager: AbstractAgentManager = Depends(get_current_agent_manager),
    session: Session = Depends(get_session)
) -> TodoAgent:
    if not agent_manager:
        raise HTTPException(status_code=503, detail="AI service is not configured. Please set an API key.")
    return TodoAgent(agent_manager, session)
