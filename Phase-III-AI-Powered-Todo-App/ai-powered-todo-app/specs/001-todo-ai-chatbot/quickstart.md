# Quickstart Guide: AI-powered Todo Chatbot

**Date**: 2026-02-09
**Feature**: [./specs/001-todo-ai-chatbot/spec.md](./specs/001-todo-ai-chatbot/spec.md)

## Summary

This guide provides a quick overview of how to set up and run the AI-powered Todo Chatbot locally for development and testing. It assumes basic familiarity with Git, Docker, Python (Poetry), and Node.js (npm/yarn).

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Git**: For cloning the repository.
*   **Docker & Docker Compose**: For running the database and potentially the backend/frontend in containers.
*   **Python 3.9+**: For the backend and AI Agent.
*   **Poetry**: Python dependency management tool (`pip install poetry`).
*   **Node.js & npm/yarn**: For the frontend (OpenAI ChatKit).

## Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd ai-powered-todo-app
    git checkout 001-todo-ai-chatbot
    ```

2.  **Environment Variables**:
    Create a `.env` file in the `backend/` directory and another in the `frontend/` directory (if separate environment variables are needed for each).
    
    **`backend/.env` (Example)**:
    ```
    DATABASE_URL="postgresql+asyncpg://user:password@host:port/database_name"
    OPENAI_API_KEY="your_openai_api_key"
    BETTER_AUTH_SECRET_KEY="your_better_auth_secret_key"
    ```
    
    **`frontend/.env` (Example, specific to OpenAI ChatKit)**:
    ```
    NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your_chatkit_domain_key"
    NEXT_PUBLIC_API_BASE_URL="http://localhost:8000" # Or your backend API URL
    ```
    *Replace placeholders with actual values.*

3.  **Database Setup (Neon Serverless PostgreSQL)**:
    *   Set up a Neon Serverless PostgreSQL instance.
    *   Obtain your database connection URL and update `DATABASE_URL` in `backend/.env`.
    *   Run database migrations (managed by Alembic, will be part of the backend setup).

4.  **Backend Setup**:
    ```bash
    cd backend/
    poetry install
    poetry shell
    alembic upgrade head # Run database migrations
    poetry run uvicorn src.main:app --reload
    ```
    The backend API should now be running locally, typically on `http://localhost:8000`.

5.  **Frontend Setup**:
    ```bash
    cd frontend/
    npm install # or yarn install
    npm run dev # or yarn dev
    ```
    The frontend (OpenAI ChatKit) should now be running locally, typically on `http://localhost:3000`.

## Usage

1.  Open your browser and navigate to the frontend URL (e.g., `http://localhost:3000`).
2.  Interact with the AI-powered Todo Chatbot using natural language commands.
3.  Monitor the backend console for logs and activity.

## Important Notes

*   Ensure all necessary API keys and secrets are securely configured via environment variables.
*   For deployment, refer to the `Deployment Notes` section in the main specification (`spec.md`) and the project's `README.md`.
*   The `001-todo-ai-chatbot` branch contains the current development for this feature.
