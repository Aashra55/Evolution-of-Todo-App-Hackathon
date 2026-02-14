# backend/src/agent/agent_logic.py
import json
import re # Added for re.search
from typing import Dict, Any, List, Optional
from uuid import UUID

from sqlmodel import Session
from fastapi import Depends # Added for get_todo_agent

from src.agent.init import OpenAIAgentManager, get_openai_agent_manager
from src.config.database import get_session
from src.mcp_tools.add_task import add_task, add_task_tool_schema
from src.mcp_tools.list_tasks import list_tasks, list_tasks_tool_schema # Import list_tasks
from src.mcp_tools.complete_task import complete_task, complete_task_tool_schema # Import complete_task
from src.mcp_tools.delete_task import delete_task, delete_task_tool_schema # Import delete_task
from src.mcp_tools.update_task import update_task, update_task_tool_schema # Import update_task

class TodoAgent:
    def __init__(self, agent_manager: OpenAIAgentManager, session: Session):
        self.agent_manager = agent_manager
        self.session = session
        self.tools = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task # Add update_task tool
        }
        self.tool_schemas = [
            add_task_tool_schema,
            list_tasks_tool_schema,
            complete_task_tool_schema,
            delete_task_tool_schema,
            update_task_tool_schema # Add update_task tool schema
        ]

    def register_tools(self):
        for schema in self.tool_schemas:
            # In a real assistant, tools would be registered with the assistant itself.
            # Here, we're just making them available for our simulated agent logic.
            # self.agent_manager.register_tool(self.tools[schema["function"]["name"]], schema)
            pass

    async def process_chat_message(self, user_id: UUID, conversation_id: UUID, message_content: str) -> str:
        """
        Processes a chat message, potentially invoking tools.
        This is a simplified mock of how an agent would operate.
        """
        # In a real OpenAI Assistant scenario, the agent_manager would handle
        # the tool calling automatically. Here, we'll simulate it for add_task and list_tasks.

        message_lower = message_content.lower()

        # Heuristic for add_task
        if "add task" in message_lower or "new task" in message_lower:
            try:
                title = ""
                description = None

                # Look for "task: <title>"
                title_match = re.search(r"task:\s*(.*?)(?:\s+description:\s*(.*))?$", message_lower)
                if title_match:
                    title = title_match.group(1).strip()
                    description = title_match.group(2).strip() if title_match.group(2) else None
                else: # Fallback for simpler "add task <title>"
                    # Find where the task title might start after "add task" or "new task"
                    idx = message_lower.find("add task")
                    if idx == -1:
                        idx = message_lower.find("new task")
                    if idx != -1:
                        title = message_content[idx + len("add task"):].strip() # Use original message_content for capitalization
                        
                        # Remove "description:" if it's there
                        desc_idx = title.lower().find("description:")
                        if desc_idx != -1:
                            description = title[desc_idx + len("description:"):].strip()
                            title = title[:desc_idx].strip()
                        
                        if title.startswith(":"): # remove leading colon if present
                            title = title[1:].strip()


                if title:
                    # Simulate tool call
                    result = self.tools["add_task"](self.session, user_id, title, description)
                    return json.dumps(result)
                else:
                    return json.dumps({"status": "error", "message": "Could not parse task title from your message."})
            except Exception as e:
                return json.dumps({"status": "error", "message": f"Error processing add task command: {e}"})
        
        # Heuristic for list_tasks - match "list" and "tasks" separately to catch variations like "list all my tasks"
        if ("list" in message_lower and "task" in message_lower) or "show tasks" in message_lower or "what do i need to do" in message_lower or "show my tasks" in message_lower:
            completed_filter: Optional[bool] = None
            if "pending" in message_lower or "uncompleted" in message_lower:
                completed_filter = False
            elif "completed" in message_lower or "done" in message_lower:
                completed_filter = True
            
            try:
                result = self.tools["list_tasks"](self.session, user_id, completed=completed_filter)
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"status": "error", "message": f"Error processing list tasks command: {e}"})

        # Heuristic for complete_task
        if "complete task" in message_lower:
            try:
                # First try to extract task ID (UUID format)
                task_id_match = re.search(r"task id:\s*([a-f0-9-]+)", message_lower)
                if task_id_match:
                    task_id = UUID(task_id_match.group(1))
                    result = self.tools["complete_task"](self.session, user_id, task_id)
                    return json.dumps(result)
                
                # Try to extract task number (e.g., "complete task 1", "complete task 2")
                task_number_match = re.search(r"complete task\s+(\d+)", message_lower)
                if task_number_match:
                    task_index = int(task_number_match.group(1)) - 1  # Convert to 0-based index
                    # Get all pending tasks
                    pending_tasks_result = self.tools["list_tasks"](self.session, user_id, completed=False)
                    if isinstance(pending_tasks_result, dict) and pending_tasks_result.get("status") == "success":
                        tasks = pending_tasks_result.get("tasks", [])
                        if task_index >= 0 and task_index < len(tasks):
                            task_id = int(tasks[task_index]["id"])
                            result = self.tools["complete_task"](self.session, user_id, task_id)
                            return json.dumps(result)
                        else:
                            return json.dumps({"status": "error", "message": f"Task number {task_index + 1} not found. You have {len(tasks)} pending task(s)."})
                    else:
                        return json.dumps({"status": "error", "message": "Could not retrieve tasks list."})
                
                # Fallback to try to find a task by title
                title_start = message_lower.find("complete the task '")
                if title_start != -1:
                    title_end = message_lower.find("'", title_start + len("complete the task '"))
                    if title_end != -1:
                        task_title = message_content[title_start + len("complete the task '"):title_end]
                        # Get all tasks and find by title
                        all_tasks_result = self.tools["list_tasks"](self.session, user_id, completed=False)
                        if isinstance(all_tasks_result, dict) and all_tasks_result.get("status") == "success":
                            tasks = all_tasks_result.get("tasks", [])
                            for task in tasks:
                                if task.get("title", "").lower() == task_title.lower():
                                    task_id = int(task["id"])
                                    result = self.tools["complete_task"](self.session, user_id, task_id)
                                    return json.dumps(result)
                            return json.dumps({"status": "error", "message": f"Task with title '{task_title}' not found."})
                
                return json.dumps({"status": "error", "message": "Could not parse task ID or number for completion. Try 'complete task 1' or 'complete task with ID: <id>'."})
            except ValueError as e:
                 return json.dumps({"status": "error", "message": f"Invalid format: {str(e)}"})
            except Exception as e:
                return json.dumps({"status": "error", "message": f"Error processing complete task command: {e}"})
        
        # Heuristic for delete_task
        if "delete task" in message_lower or "remove task" in message_lower:
            try:
                task_id_match = re.search(r"task id:\s*([a-f0-9-]+)", message_lower)
                if task_id_match:
                    task_id = UUID(task_id_match.group(1))
                    result = self.tools["delete_task"](self.session, user_id, task_id)
                    return json.dumps(result)
                else:
                    # Fallback for "delete task <title>"
                    title_match = re.search(r"(?:delete|remove)\s+(?:the\s+task\s+)?['\"]?(.*?)(?:['\"]?)$", message_lower)
                    if title_match and title_match.group(1):
                        task_title = title_match.group(1).strip()
                        # In a real scenario, need to resolve title to ID
                        return json.dumps({"status": "error", "message": f"Tool call for 'delete_task' by title '{task_title}' not yet implemented. Please provide a task ID."})
                    
                    return json.dumps({"status": "error", "message": "Could not parse task ID or title for deletion. Please specify 'delete task with ID: <uuid>' or by title if implemented."})
            except ValueError:
                return json.dumps({"status": "error", "message": "Invalid UUID format for task ID."})
            except Exception as e:
                return json.dumps({"status": "error", "message": f"Error processing delete task command: {e}"})

        # Heuristic for update_task
        if "update task" in message_lower:
            try:
                task_id_match = re.search(r"task id:\s*([a-f0-9-]+)", message_lower)
                if task_id_match:
                    task_id = UUID(task_id_match.group(1))
                    
                    # Extract title, description, completed status
                    new_title = None
                    new_description = None
                    new_completed = None

                    title_match = re.search(r"new title:\s*(.*?)(?:\s+(?:new description|completed):|$)", message_lower)
                    if title_match:
                        new_title = title_match.group(1).strip()

                    description_match = re.search(r"new description:\s*(.*?)(?:\s+(?:new title|completed):|$)", message_lower)
                    if description_match:
                        new_description = description_match.group(1).strip()

                    completed_match = re.search(r"completed:\s*(true|false)", message_lower)
                    if completed_match:
                        new_completed = completed_match.group(1).lower() == "true"
                    
                    if not any([new_title, new_description, new_completed]):
                         return json.dumps({"status": "error", "message": "No update parameters provided for task. Specify 'new title:', 'new description:', or 'completed: true/false'."})


                    result = self.tools["update_task"](self.session, user_id, task_id, title=new_title, description=new_description, completed=new_completed)
                    return json.dumps(result)
                else:
                    return json.dumps({"status": "error", "message": "Could not parse task ID for update. Please specify 'update task with ID: <uuid>' and parameters like 'new title: <title>'."})
            except ValueError:
                return json.dumps({"status": "error", "message": "Invalid UUID format for task ID."})
            except Exception as e:
                return json.dumps({"status": "error", "message": f"Error processing update task command: {e}"})

        # Fallback to general AI response if no tool is matched
        print(f"No tool matched for message: {message_content}. Falling back to AI response.")
        try:
            ai_response = await self.agent_manager.process_message(str(user_id), str(conversation_id), message_content)
            print(f"AI response received: {ai_response[:200] if ai_response else 'None'}...")
            return ai_response if ai_response else "I received your message but couldn't generate a response. Please try again."
        except Exception as e:
            error_msg = f"Error getting AI response: {str(e)}"
            print(f"Error in AI response: {error_msg}")
            return error_msg

async def get_todo_agent(
    agent_manager: OpenAIAgentManager = Depends(get_openai_agent_manager),
    session: Session = Depends(get_session)
) -> TodoAgent:
    agent = TodoAgent(agent_manager, session)
    agent.register_tools()
    return agent
