from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Callable, List, Optional

# Placeholder for MCP SDK integration
class ToolInvocation(BaseModel):
    tool_name: str
    tool_args: Dict[str, Any]

class ToolResponse(BaseModel):
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None

# In a real MCP SDK, these would be managed by the SDK itself
REGISTERED_TOOLS: Dict[str, Callable] = {}

def register_tool(name: str):
    def decorator(func: Callable):
        REGISTERED_TOOLS[name] = func
        return func
    return decorator


router = APIRouter(
    prefix="/mcp",
    tags=["mcp"]
)

@router.post("/invoke", response_model=ToolResponse)
async def invoke_mcp_tool(invocation: ToolInvocation, request: Request):
    if invocation.tool_name not in REGISTERED_TOOLS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{invocation.tool_name}' not found."
        )
    
    tool_func = REGISTERED_TOOLS[invocation.tool_name]
    try:
        # In a real scenario, tool_func might need a session or other dependencies
        # For simplicity, pass args directly
        result = await tool_func(**invocation.tool_args)
        return ToolResponse(tool_name=invocation.tool_name, success=True, output=result)
    except Exception as e:
        return ToolResponse(tool_name=invocation.tool_name, success=False, output=None, error=str(e))

@router.get("/tools", response_model=List[str])
async def list_mcp_tools():
    return list(REGISTERED_TOOLS.keys())