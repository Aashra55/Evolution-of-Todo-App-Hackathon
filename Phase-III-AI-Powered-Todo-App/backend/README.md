# Todo AI Chatbot Backend

This is the backend service for the Todo AI Chatbot, built using FastAPI and SQLModel. It handles API requests, interacts with the PostgreSQL database, and hosts the MCP server and tools.

## Development Setup

1.  **Install Poetry**: `pip install poetry`
2.  **Install Dependencies**: `poetry install`
3.  **Run Migrations**: (Once Alembic is configured) `poetry run alembic upgrade head`
4.  **Run Server**: `poetry run uvicorn main:app --reload`
