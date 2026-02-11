# AI-Powered Todo Chatbot

This project features an AI-powered Todo Chatbot designed to help users manage their tasks efficiently through natural language conversations. The application boasts a modern architecture with a separate frontend and backend, leveraging cutting-edge AI capabilities to understand and execute task-related commands.

## Features

*   **Natural Language Task Management**: Interact with your todo list using simple, conversational commands.
*   **Comprehensive Task Operations**: Easily **add**, **view**, **mark as complete**, **delete**, and **update** your tasks.
*   **Interactive Chat Interface**: A user-friendly chat display where you can converse with the AI and see your messages and AI responses.
*   **Dynamic Task List Panel**: Tasks are automatically displayed and updated in a dedicated panel, reflecting their status (pending, completed).
*   **Instant Feedback**: Receive notifications and toasts for successful operations or error messages.
*   **Responsive Design**: A clean, minimalistic, and responsive user interface, ensuring a seamless experience across desktop and mobile devices.
*   **Stateless Backend**: The backend is designed to be stateless, promoting scalability and maintainability.
*   **Persistent Data Storage**: All tasks, conversations, and messages are stored persistently in a robust database.
*   **AI Integration**: Powered by the OpenAI Agents SDK for intelligent natural language understanding and task execution.
*   **Micro-Capability Platform (MCP) Tools**: Utilizes custom MCP tools for precise task operations.
*   **Secure Authentication**: Integrates with "Better Auth" for user authentication.

## Tech Stack

The application is built with a robust and scalable tech stack:

### Backend (Python FastAPI)

*   **Language**: Python 3.9+
*   **Web Framework**: FastAPI
*   **ASGI Server**: Uvicorn
*   **ORM**: SQLModel
*   **Database**: Neon Serverless PostgreSQL (via Psycopg adapter)
*   **Dependency Management**: Poetry
*   **AI Integration**: OpenAI Agents SDK (using `openai` package)
*   **Authentication**: Custom integration with "Better Auth" concepts (using `python-jose`, `passlib`)
*   **Environment Variables**: python-dotenv
*   **Database Migrations**: Alembic
*   **Containerization**: Docker

### Frontend (Next.js with React)

*   **Framework**: Next.js (used for project structure, but currently plain React components)
*   **Library**: React, React-DOM
*   **UI/UX**: Custom components based on functional requirements
*   **HTTP Client**: Axios
*   **UUID Generation**: `uuid`
*   **Dependency Management**: npm / yarn

## Project Structure

The project is organized into `backend` and `frontend` directories, along with documentation and configuration files:

```
ai-powered-todo-app/
├── backend/                  # FastAPI backend and AI Agent services
│   ├── src/                  # Python source code
│   │   ├── api/              # FastAPI endpoints (e.g., chat.py)
│   │   ├── agent/            # OpenAI Agents SDK integration logic (init.py, agent_logic.py)
│   │   ├── config/           # Database and logging configuration (database.py, logging.py)
│   │   ├── middleware/       # Custom FastAPI middleware (error_handler.py)
│   │   ├── models/           # SQLModel database models (Task, Conversation, Message)
│   │   └── mcp_tools/        # Implementations of MCP tools (add_task, list_tasks, etc.)
│   ├── tests/                # Unit, integration, and API tests
│   ├── Dockerfile            # Dockerization for the backend
│   └── pyproject.toml        # Poetry for Python dependency management
├── frontend/                 # Next.js frontend application
│   ├── src/                  # React components, pages, services, styles
│   │   ├── components/       # UI components (App.js, ChatInput, ChatDisplay, TaskListPanel, Notifications)
│   │   ├── pages/            # Next.js pages (index.js)
│   │   └── styles/           # Styling (responsive.css, Notifications.css)
│   ├── public/               # Static assets
│   ├── package.json          # npm/yarn for JavaScript dependency management
│   └── .env                  # Environment variables for frontend
├── specs/                    # Specification documents for features
│   └── 001-todo-ai-chatbot/  # Feature-specific documentation
│       ├── spec.md           # Detailed feature specification
│       ├── plan.md           # Implementation plan
│       ├── tasks.md          # Detailed development tasks
│       ├── data-model.md     # Database data model definitions
│       ├── quickstart.md     # Quickstart guide
│       ├── research.md       # Research notes
│       └── contracts/        # API contracts (e.g., openapi.yaml)
├── history/                  # Prompt History Records (PHRs) and Architectural Decision Records (ADRs)
└── .specify/                 # Gemini CLI configuration and templates
```

## Getting Started

Follow these instructions to set up and run the AI-Powered Todo Chatbot locally.

### Prerequisites

*   **Git**: For cloning the repository.
*   **Python 3.9+**: For the backend and AI Agent.
*   **Poetry**: Python dependency management tool (`pip install poetry`).
*   **Node.js & npm (or Yarn)**: For the frontend.
*   **Neon Serverless PostgreSQL**: A database instance.
*   **Gemini API Key**: Required for the AI Agent.

### Cloning the Repository

```bash
# Clone the entire repository
git clone https://github.com/Aashra55/Evolution-of-Todo-App-Hackathon.git
cd Evolution-of-Todo-App-Hackathon/Phase-III-AI-Powered-Todo-App/todo-ai-chatbot
```

### Backend Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```
2.  **Initialize Python virtual environment and install dependencies**:
    ```bash
    python -m venv .venv
    ./.venv/Scripts/activate # On Windows
    source ./.venv/bin/activate # On Linux/macOS
    pip install poetry
    poetry install
    pip install python-jose passlib # For authentication utilities
    pip install openai sqlmodel sqlalchemy # For OpenAI SDK and ORM
    ```
3.  **Create necessary directories**:
    ```bash
    mkdir -p src/api src/agent src/middleware src/models src/mcp_tools
    ```
4.  **Configure Environment Variables**:
    Create a `.env` file in the `backend/` directory with the following variables:
    ```
    DATABASE_URL="postgresql+psycopg://user:password@host:port/database_name"
    OPENAI_API_KEY="your_gemini_api_key" # Use your Gemini API key here
    OPENAI_API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/" # Gemini API endpoint
    SECRET_KEY="your_super_secret_key_for_jwt" 
    ```
    *Replace placeholders with your actual database connection string, Gemini API key, and a strong secret key.*
5.  **Run Database Initialization**:
    This project uses SQLModel. Ensure your `DATABASE_URL` is correctly configured in `backend/.env`.
    ```bash
    # This will create tables based on your SQLModel definitions
    # It should be run after creating your database in Neon and setting DATABASE_URL
    # You might need to add a command to backend/src/main.py or a separate script to call create_db_and_tables()
    # For now, manually ensure the create_db_and_tables() function is called on startup.
    # (Already handled in backend/src/main.py lifespan event)
    ```
6.  **Run the Backend Server**:
    ```bash
    poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The backend API will be accessible at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install
    # or if you prefer yarn
    yarn install
    ```
    *(Note: `axios` and `uuid` are already included in `package.json`.)*
3.  **Configure Environment Variables**:
    Create a `.env.local` file in the `frontend/` directory with the following variables:
    ```
    NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
    ```
    *Ensure `NEXT_PUBLIC_BACKEND_URL` points to your running backend instance.*
4.  **Run the Frontend Development Server**:
    ```bash
    npm run dev
    # or
    yarn dev
    ```
    The frontend application will be accessible at `http://localhost:3000` (or another port if configured).

## Usage

1.  Ensure both the backend and frontend servers are running.
2.  Open your browser and navigate to the frontend URL (e.g., `http://localhost:3000`).
3.  Interact with the AI-powered Todo Chatbot using natural language commands in the chat input.
    *   **Add Task**: "Add task: Buy groceries, description: Milk, Eggs, and Bread."
    *   **List Tasks**: "List all my tasks" or "Show me my pending tasks."
    *   **Complete Task**: "Complete task with ID: [task_uuid]"
    *   **Delete Task**: "Delete task with ID: [task_uuid]"
    *   **Update Task**: "Update task with ID: [task_uuid], new title: Finish report, new description: Finalize Q3 earnings report."
    *   Observe tasks updating in the Task List Panel and receive notifications.

## Development Notes

### Running Tests

#### Backend (Python)

To run unit and integration tests for the backend, navigate to the `backend/` directory and use `pytest`:

```bash
cd backend
poetry run pytest tests/unit/mcp_tools/test_mcp_tools.py
poetry run pytest tests/integration/test_api_endpoints.py
# Or to run all tests
poetry run pytest tests/
```

#### Frontend (JavaScript/React)

To run unit tests for the frontend components, navigate to the `frontend/` directory and use `jest` (or your configured test runner):

```bash
cd frontend
npm test # or yarn test
```

### Code Style and Linting

*   **Python**: This project uses `black` for formatting and `flake8` for linting.
*   **JavaScript**: This project uses `ESLint` and `Prettier`.

## API Reference

The backend exposes a single primary endpoint for chat interactions:

### `POST /api/{user_id}/chat`

*   **Description**: Sends a message to the AI chatbot to process natural language commands.
*   **Parameters**:
    *   `user_id` (path): Unique identifier for the user (UUID format).
*   **Request Body (`application/json`)**:
    ```json
    {
      "message": "Your natural language command here, e.g., 'Add a new task: Buy groceries'",
      "conversation_id": "optional_uuid_of_conversation"
    }
    ```
*   **Response (`application/json`)**:
    ```json
    {
      "response": "AI Agent's response. This will be a JSON string if a tool was called, or a natural language string otherwise.",
      "conversation_id": "uuid_of_conversation",
      "tool_calls": [
        // Optional: details of any internal tool calls made by the AI agent (future implementation)
      ]
    }
    ```
    For a full API specification, refer to `specs/001-todo-ai-chatbot/contracts/openapi.yaml`.

## Conclusion

The AI-Powered Todo Chatbot provides an intuitive and efficient way to manage your daily tasks using the power of natural language. We encourage you to explore its features, contribute to its development, and provide feedback to help us improve.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


