# Quick Start Guide

This guide provides the basic steps to get the full-stack to-do application running locally.

## Project Overview

This is a modern, full-stack web application featuring:
- A **Next.js** frontend for a responsive user interface.
- A **FastAPI** backend to provide a RESTful API.
- A **Neon Serverless PostgreSQL** database for persistent storage.

## Prerequisites

Before you begin, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (LTS version)
- [Python](https://www.python.org/) (3.9+)
- [Poetry](https://python-poetry.org/) for Python dependency management
- An account with [Neon](https://neon.tech/) to get a database connection string.

## Backend Setup (FastAPI)

1.  **Navigate to the backend directory**:
    ```bash
    cd src/backend 
    ```
    *(Note: This directory will be created in the implementation phase)*

2.  **Create an environment file**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

3.  **Configure environment variables**:
    Open the `.env` file and fill in the following values:
    - `DATABASE_URL`: Your Neon PostgreSQL connection string.
    - `SECRET_KEY`: A long, random string for JWT signing. You can generate one using `openssl rand -hex 32`.

4.  **Install dependencies**:
    ```bash
    poetry install
    ```

5.  **Run the database migrations**:
    *(This command will be created during implementation)*
    ```bash
    poetry run alembic upgrade head
    ```

6.  **Run the backend server**:
    ```bash
    poetry run uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

## Frontend Setup (Next.js)

1.  **Navigate to the frontend directory**:
    ```bash
    cd src/frontend
    ```
    *(Note: This directory will be created in the implementation phase)*

2.  **Create an environment file**:
    Create a new file named `.env.local`.

3.  **Configure environment variables**:
    Add the following line to your `.env.local` file, pointing to your running backend:
    ```
    NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
    ```

4.  **Install dependencies**:
    ```bash
    npm install
    ```

5.  **Run the frontend development server**:
    ```bash
    npm run dev
    ```

## Accessing the Application

Once both the backend and frontend are running, you can access the application in your browser at:
[http://localhost:3000](http://localhost:3000)
