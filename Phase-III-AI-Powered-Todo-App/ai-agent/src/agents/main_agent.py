import os
from typing import Dict, Any, Optional
import json
from uuid import UUID

from ai_agent.src.agents.tool_handler import ToolHandler # NEW


class Agent:
    def __init__(self, name: str, tools: Dict[str, Any]):
        self.name = name
        self.tools = tools
        self.conversation_history = [] # In a real app, this would be loaded/saved
        self.tool_handler = ToolHandler() # NEW


    async def chat(self, user_message: str, conversation_id: Optional[str] = None, current_user_id: Optional[UUID] = None) -> Dict[str, Any]: # NEW: added current_user_id
        # Simulate intent recognition and tool invocation
        print(f"Agent received: {user_message} (Conversation ID: {conversation_id}, User ID: {current_user_id})")

        # Basic keyword-based intent detection for demo
        # In a real agent, this would be sophisticated NLP/LLM based intent extraction
        
        user_id_str = str(current_user_id) if current_user_id else os.getenv("DEFAULT_USER_ID", "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6")

        if "create todo" in user_message.lower():
            description = user_message.replace("create todo", "").strip()
            if not description:
                return {"reply": "What would you like to add to your todo list?"}
            
            tool_args = {"user_id": user_id_str, "description": description}
            tool_response = await self.tool_handler.invoke_tool("create_todo", tool_args) # NEW: Use ToolHandler
            
            if tool_response.get("success"):
                todo_data = tool_response["output"]
                return {"reply": f"Todo '{todo_data['description']}' created with ID {todo_data['id']}."}
            else:
                return {"reply": f"Failed to create todo: {tool_response.get('error', 'Unknown error')}"}

        elif "list todos" in user_message.lower():
            tool_args = {"user_id": user_id_str}
            tool_response = await self.tool_handler.invoke_tool("list_todos_by_user", tool_args) # NEW: Use ToolHandler

            if tool_response.get("success"):
                todos = tool_response["output"]
                if todos:
                    todo_list_str = "\n".join([f"- {t['description']} ({t['status']})" for t in todos])
                    return {"reply": f"Here are your todos:\n{todo_list_str}"}
                else:
                    return {"reply": "You have no todos."}
            else:
                return {"reply": f"Failed to list todos: {tool_response.get('error', 'Unknown error')}"}
        
        elif "update todo" in user_message.lower():
            # This is a very basic simulation; a real agent would extract todo_id, new_description, etc.
            return {"reply": "To update a todo, I need its ID and the new details (description, status, due date). E.g., 'update todo ID-XYZ status completed'"}

        elif "delete todo" in user_message.lower():
            # Similar basic simulation
            return {"reply": "To delete a todo, I need its ID. E.g., 'delete todo ID-XYZ'"}

        elif "hello" in user_message.lower():
            return {"reply": "Hello there! How can I help you with your todos today?"}
        else:
            return {"reply": "I'm not sure how to handle that. Can you ask about creating, listing, updating, or deleting todos?"}


def initialize_agent():
    available_tools = {
        "create_todo": "Creates a todo item",
        "get_todo": "Retrieves a todo item",
        "list_todos_by_user": "Lists all todos for a user",
        "update_todo": "Updates a todo item",
        "delete_todo": "Deletes a todo item",
    }
    return Agent(name="TodoBot", tools=available_tools)