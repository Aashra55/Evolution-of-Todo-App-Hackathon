from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.database import create_db_and_tables
from src.config.logging import configure_logging
from src.middleware.error_handler import ErrorHandlingMiddleware
from src.api import chat
from src.agent.init import openai_agent_manager

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Add error handling middleware
app.add_middleware(ErrorHandlingMiddleware)

# Include routers
app.include_router(chat.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}