import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
import json

from ai_agent.src.agents.main_agent import initialize_agent, Agent
from ai_agent.src.agents.tool_handler import ToolHandler


@pytest.fixture
def mock_tool_handler():
    with patch('ai_agent.src.agents.main_agent.ToolHandler') as MockToolHandler:
        instance = MockToolHandler.return_value
        instance.invoke_tool = AsyncMock()
        yield instance

@pytest.fixture
def agent(mock_tool_handler):
    # Pass the mocked tool_handler to the agent
    _agent = initialize_agent()
    _agent.tool_handler = mock_tool_handler
    return _agent


@pytest.fixture
def test_user_id():
    return uuid4()

@pytest.mark.asyncio
async def test_agent_hello_message(agent: Agent, test_user_id):
    response = await agent.chat("hello", current_user_id=test_user_id)
    assert "Hello there!" in response["reply"]
    agent.tool_handler.invoke_tool.assert_not_called()

@pytest.mark.asyncio
async def test_agent_create_todo_success(agent: Agent, mock_tool_handler, test_user_id):
    description = "Buy milk"
    mock_tool_handler.invoke_tool.return_value = {
        "tool_name": "create_todo",
        "success": True,
        "output": {"id": str(uuid4()), "description": description, "status": "pending", "user_id": str(test_user_id)},
        "error": None
    }
    
    response = await agent.chat(f"create todo {description}", current_user_id=test_user_id)
    assert description in response["reply"]
    assert "created" in response["reply"]
    mock_tool_handler.invoke_tool.assert_called_once_with("create_todo", {"user_id": str(test_user_id), "description": description})

@pytest.mark.asyncio
async def test_agent_create_todo_failure(agent: Agent, mock_tool_handler, test_user_id):
    description = "Buy bread"
    mock_tool_handler.invoke_tool.return_value = {
        "tool_name": "create_todo",
        "success": False,
        "output": None,
        "error": "Database error"
    }
    
    response = await agent.chat(f"create todo {description}", current_user_id=test_user_id)
    assert "Failed to create todo: Database error" in response["reply"]
    mock_tool_handler.invoke_tool.assert_called_once_with("create_todo", {"user_id": str(test_user_id), "description": description})

@pytest.mark.asyncio
async def test_agent_list_todos_success(agent: Agent, mock_tool_handler, test_user_id):
    mock_tool_handler.invoke_tool.return_value = {
        "tool_name": "list_todos_by_user",
        "success": True,
        "output": [
            {"id": str(uuid4()), "description": "Buy milk", "status": "pending", "user_id": str(test_user_id)},
            {"id": str(uuid4()), "description": "Walk dog", "status": "completed", "user_id": str(test_user_id)}
        ],
        "error": None
    }
    
    response = await agent.chat("list todos", current_user_id=test_user_id)
    assert "Here are your todos" in response["reply"]
    assert "Buy milk (pending)" in response["reply"]
    assert "Walk dog (completed)" in response["reply"]
    mock_tool_handler.invoke_tool.assert_called_once_with("list_todos_by_user", {"user_id": str(test_user_id)})

@pytest.mark.asyncio
async def test_agent_list_todos_empty(agent: Agent, mock_tool_handler, test_user_id):
    mock_tool_handler.invoke_tool.return_value = {
        "tool_name": "list_todos_by_user",
        "success": True,
        "output": [],
        "error": None
    }
    
    response = await agent.chat("list todos", current_user_id=test_user_id)
    assert "You have no todos." in response["reply"]
    mock_tool_handler.invoke_tool.assert_called_once_with("list_todos_by_user", {"user_id": str(test_user_id)})

@pytest.mark.asyncio
async def test_agent_unknown_command(agent: Agent, test_user_id):
    response = await agent.chat("what is the weather like?", current_user_id=test_user_id)
    assert "I'm not sure how to handle that" in response["reply"]
    agent.tool_handler.invoke_tool.assert_not_called()
