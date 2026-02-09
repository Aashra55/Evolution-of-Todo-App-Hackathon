# Quickstart Guide: Todo AI Chatbot (Phase III – Basic Level)

**Date**: 2026-02-07

## Overview

This guide provides instructions to quickly set up and interact with the basic functionality of the Todo AI Chatbot API. It covers environment setup, running tests, and basic API interaction examples.

## 1. Environment Setup

### Prerequisites

*   Python 3.10+
*   Node.js (for Frontend)
*   Docker (for local database setup, if not using remote Neon DB)
*   Git

### Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### Backend Setup (Python FastAPI)

1.  **Install Poetry**: `pip install poetry` (if not already installed)
2.  **Install Dependencies**: `cd backend && poetry install`
3.  **Database Setup**:
    *   **Option A: Local PostgreSQL (Docker)**:
        ```bash
        docker run --name local-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=todo_db -p 5432:5432 -d postgres
        ```
    *   **Option B: Neon Serverless PostgreSQL**: Obtain connection string from Neon.
4.  **Configuration**: Set environment variables for database connection (e.g., `DATABASE_URL=postgresql://user:password@localhost:5432/todo_db`) and JWT `SECRET_KEY`.
5.  **Run Migrations**: `cd backend && poetry run alembic upgrade head` (This assumes you've manually edited the initial migration script).
6.  **Start Backend Server**: `cd backend && poetry run uvicorn main:app --reload`

### Frontend Setup (OpenAI ChatKit)

1.  **Install Node.js dependencies**: `cd frontend && npm install`
2.  **Start Frontend Development Server**: `cd frontend && npm start`

### AI Agent Setup (OpenAI Agents SDK)

1.  **Install Poetry**: `pip install poetry` (if not already installed)
2.  **Install Dependencies**: `cd ai-agent && poetry install`
3.  **Configuration**: Set environment variables `MCP_SERVER_URL` (e.g., `http://localhost:8000/mcp/invoke`) and `DEFAULT_USER_ID`.
4.  **Run AI Agent (standalone for testing/development)**: `cd ai-agent && poetry run python src/agents/main_agent.py` (Note: This is a simplified run command for the placeholder agent).

## 2. Running Tests

### Backend Tests

```bash
cd backend
poetry run pytest tests/backend/
```

### AI Agent Tests

```bash
cd ai-agent
poetry run pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 3. Basic API Interaction

Use `curl` or a tool like Postman/Insomnia. Ensure backend is running.

### 3.1. Get an Authentication Token

First, register/login a user to obtain a JWT token.

```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/json" \
     -d '{ "username": "testuser", "password": "testpassword", "email": "test@example.com" }'
```
*Save the `access_token` from the response.*

### 3.2. Create a Todo

Replace `<YOUR_AUTH_TOKEN>` with the token obtained above.

```bash
curl -X POST "http://localhost:8000/todos/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <YOUR_AUTH_TOKEN>" \
     -d '{ "description": "Buy groceries", "due_date": "2026-02-09T18:00:00Z" }'
```
*Save the `id` of the created todo.*

### 3.3. List Todos for Your User

Replace `<YOUR_USER_ID>` with the `user_id` obtained during login/token creation (or infer from token payload).

```bash
curl -X GET "http://localhost:8000/todos/user/<YOUR_USER_ID>" \
     -H "Authorization: Bearer <YOUR_AUTH_TOKEN>"
```

### 3.4. Update a Todo

Replace `<TODO_ID>` with the ID of a todo you want to update.

```bash
curl -X PUT "http://localhost:8000/todos/<TODO_ID>" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <YOUR_AUTH_TOKEN>" \
     -d '{ "status": "completed" }'
```

### 3.5. Delete a Todo

Replace `<TODO_ID>` with the ID of a todo you want to delete.

```bash
curl -X DELETE "http://localhost:8000/todos/<TODO_ID>" \
     -H "Authorization: Bearer <YOUR_AUTH_TOKEN>"
```

### 3.6. Interact with the Chat Endpoint

This requires the backend to be running.

```bash
curl -X POST "http://localhost:8000/chat/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <YOUR_AUTH_TOKEN>" \
     -d '{ "message": "create todo finish quickstart guide" }'
```
*Note the `conversation_id` from the response for follow-up messages.*

## Next Steps

*   Explore further API functionality.
*   Continue frontend development.