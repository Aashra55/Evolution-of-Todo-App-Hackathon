from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from backend.src.config.database import create_db_and_tables
from backend.src.config.logging import configure_logging
from backend.src.middleware.error_handler import ErrorHandlingMiddleware
from backend.src.api import chat
from backend.src.agent.init import openai_agent_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup events
    configure_logging()
    print("Application startup: Configuring logging, creating database tables...")
    create_db_and_tables()
    await openai_agent_manager.initialize_assistant(instructions="You are an AI-powered Todo Chatbot.")
    yield
    # Shutdown events
    print("Application shutdown: Cleaning up resources...")

app = FastAPI(lifespan=lifespan)

# Add middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=ErrorHandlingMiddleware)

# Include routers
app.include_router(chat.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}