# Backend - Todo Web App

This directory contains the FastAPI backend for the Todo Web App.

## Features

- User authentication (signup, login, JWT token generation)
- Task management (create, read, update, delete tasks)
- Data isolation (users can only access their own tasks)
- Database migrations with Alembic
- Environment variable management with python-dotenv

## Setup

Follow these steps to set up and run the backend:

1.  **Navigate to the backend directory:**
    ```bash
    cd src/backend
    ```

2.  **Install Poetry (if you haven't already):**
    Poetry is used for dependency management.
    ```bash
    pip install poetry
    ```
    If you encounter issues, refer to the [Poetry documentation](https://python-poetry.org/docs/#installation).

3.  **Install dependencies:**
    ```bash
    poetry install
    ```

4.  **Environment Variables:**
    Create a `.env` file in the `src/backend` directory based on the `.env.example` file:
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file and set the `DATABASE_URL` and `SECRET_KEY`. For local development, you can use SQLite:
    ```
    DATABASE_URL="sqlite:///./test.db"
    SECRET_KEY="your_super_secret_key"
    ```
    Ensure `SECRET_KEY` is a strong, random string.

5.  **Database Migrations:**
    Apply database migrations using Alembic:
    ```bash
    poetry run alembic upgrade head
    ```

## Running the Application

To start the FastAPI application:

```bash
poetry run uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.
