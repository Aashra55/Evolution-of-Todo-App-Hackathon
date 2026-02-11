# AI-Powered Todo App Chatbot

## Description
This project is an AI-powered Todo Application Chatbot, developed as part of the Evolution-of-Todo-App-Hackathon. It allows users to interact with an AI assistant to manage their tasks through a conversational interface. The application features a frontend built with Next.js/React and a backend API powered by Python FastAPI.

## Features
*   **AI Chatbot Interface:** Converse with an AI to manage your todo list.
*   **Task Management:** Add, view, update, and mark tasks as complete through chat commands.
*   **Dynamic Task Display:** Clearly separates and visualizes pending and completed tasks.
*   **Modern UI:** Features a neon-themed dark aesthetic for an engaging user experience.
*   **Backend API:** A robust API handles task management and AI interactions, likely defined by `specs/contracts/openapi.yaml`.

## Technologies Used
*   **Frontend:** Next.js, React, Tailwind CSS (via CDN), React Icons, Axios, OpenAI SDK
*   **Backend:** Python, FastAPI, Uvicorn, SQLModel, PostgreSQL (using `psycopg`), Alembic (for database migrations), OpenAI API, Pydantic, Python-jose, Passlib

## Setup & Installation

### Prerequisites
*   Node.js and npm/yarn
*   Python 3.9+
*   Poetry (for Python dependency management)
*   Docker (recommended for PostgreSQL database)

### Backend Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <project_directory>/todo-ai-chatbot
    ```
2.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
3.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```
4.  **Set up the database:**
    *   **Using Docker (Recommended):** Ensure you have Docker and Docker Compose installed. You may need to adapt or create a `docker-compose.yml` if one doesn't exist for the database. Run:
        ```bash
        docker-compose up -d db # (Assuming 'db' service is defined for PostgreSQL)
        ```
    *   **Manual PostgreSQL Setup:** Instructions for manual PostgreSQL setup would go here if Docker is not used.
5.  **Set environment variables:** Create a `.env` file in the `backend/` directory with necessary variables (e.g., `DATABASE_URL`, `OPENAI_API_KEY`). Refer to `.env.example` if available.
6.  **Run database migrations (if using Alembic):**
    ```bash
    poetry run alembic upgrade head
    ```
7.  **Run the backend server:**
    ```bash
    poetry run uvicorn src.main:app --reload
    ```

### Frontend Setup
1.  **Navigate to the frontend directory:**
    ```bash
    cd ../frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install  # or yarn install
    ```
3.  **Set environment variables:** Create a `.env.local` file in the `frontend/` directory with necessary variables (e.g., `NEXT_PUBLIC_API_URL` pointing to your backend).
4.  **Run the frontend development server:**
    ```bash
    npm run dev # or yarn dev
    ```

## Usage
1.  Ensure both the backend and frontend are running.
2.  Open your browser to the frontend URL (typically `http://localhost:3000` or as specified by the frontend's dev server).
3.  Interact with the AI chatbot to manage your tasks.

## Contributing
Please refer to the `CONTRIBUTING.md` file for guidelines on how to contribute to this project. (Note: `CONTRIBUTING.md` file may need to be created).

## License
This project is licensed under the MIT License - see the `LICENSE` file for details. (Note: LICENSE file may need to be created).

---
