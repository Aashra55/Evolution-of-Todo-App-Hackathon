import os
import httpx
from typing import Dict, Any, Optional

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp/invoke")

class ToolHandler:
    async def invoke_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "tool_name": tool_name,
            "tool_args": tool_args
        }
        print(f"Invoking MCP tool: {tool_name} with args: {tool_args}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(MCP_SERVER_URL, json=payload)
                response.raise_for_status() # Raise an exception for bad status codes
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error invoking tool {tool_name}: {e.response.status_code} - {e.response.text}"}
        except httpx.RequestError as e:
            return {"error": f"Network error invoking tool {tool_name}: {e}"}
        except Exception as e:
            return {"error": f"Unexpected error invoking tool {tool_name}: {e}"}
