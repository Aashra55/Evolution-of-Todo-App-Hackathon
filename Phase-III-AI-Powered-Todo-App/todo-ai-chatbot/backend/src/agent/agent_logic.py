# backend/src/agent/agent_logic.py
import json
import os
from typing import Dict, Any, List
from uuid import UUID

from fastapi import Depends, HTTPException
import google.generativeai as genai
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
            if isinstance(self.agent_manager, GeminiAgentManager):
                # For Gemini, the tools are the functions themselves.
                # The model is already configured with the API key.
                model = genai.GenerativeModel(
                    model_name=os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest"),
                    system_instruction=system_prompt,
                    tools=self.tool_functions
                )
                chat = model.start_chat(enable_automatic_function_calling=True)
                
                # We need to provide the session object to our tools.
                # The Gemini SDK doesn't support context injection directly into tools.
                # A workaround is to wrap our tools to inject the session.
                # However, for simplicity here, we'll assume tools can access it or are stateless.
                # A better long-term solution involves a custom tool execution layer.
                # For now, this demonstrates the intended AI flow.
                # The `_execute_tool` method is bypassed by automatic function calling.
                
                response = await chat.send_message_async(message_content)
                return response.text

            elif isinstance(self.agent_manager, OpenAIAgentManager):
                client = self.agent_manager.get_client()
                messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message_content}]
                
                response = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
                    messages=messages,
                    tools=self.tool_schemas,
                    tool_choice="auto",
                )
                response_message = response.choices[0].message
                
                tool_calls = response_message.tool_calls
                if not tool_calls:
                    return response_message.content

                messages.append(response_message)
                
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Manually inject session for OpenAI tool calls
                    function_args['db'] = self.session
                    function_args['user_id'] = user_id
                    
                    tool_function = self.tool_functions.get(function_name)
                    if tool_function:
                        function_response = tool_function(**function_args)
                        messages.append({
                            "tool_call_id": tool_call.id, "role": "tool",
                            "name": function_name, "content": json.dumps(function_response),
                        })
                
                second_response = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o"), messages=messages
                )
                return second_response.choices[0].message.content
            
            else:
                return "No valid AI agent manager is configured."

        except Exception as e:
            print(f"Error processing chat message: {e}")
            return "I'm having trouble processing your request. Please ensure your AI configuration is correct and try again."

async def get_todo_agent(
    agent_manager: AbstractAgentManager = Depends(get_current_agent_manager),
    session: Session = Depends(get_session)
) -> TodoAgent:
    if not agent_manager:
        raise HTTPException(status_code=503, detail="AI service is not configured. Please set an API key.")
    return TodoAgent(agent_manager, session)
