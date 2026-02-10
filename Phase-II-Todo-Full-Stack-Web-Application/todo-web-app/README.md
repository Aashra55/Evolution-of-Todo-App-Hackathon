# Full-Stack Todo Web Application

A modern, full-stack Todo application built with Next.js, React, and FastAPI, featuring user authentication and task management.

## Features

*   **User Authentication:** Secure user registration and login functionality.
*   **User Profile Management:** Dedicated page for managing user profiles.
*   **Task Management:**
    *   Create new tasks.
    *   View existing tasks.
    *   Update task descriptions and completion status.
    *   Delete tasks.
*   **Interactive Dashboard:** A dashboard for users to efficiently manage their tasks.
*   **Responsive Design:** Built with Tailwind CSS for a modern and adaptive user interface.

## Tech Stack

### Frontend

*   **Framework:** Next.js
*   **Library:** React
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS
*   **Icons:** React Icons

### Backend

*   **Language:** Python 3.10+
*   **Web Framework:** FastAPI
*   **ORM:** SQLModel
*   **Database:** PostgreSQL (via `psycopg2-binary`)
*   **Authentication:** JWT (JSON Web Tokens) with `python-jose` and `passlib` for password hashing (`bcrypt`).
*   **ASGI Server:** Uvicorn
*   **Database Migrations:** Alembic

## Application Structure

The project is organized into `src/backend` for the FastAPI application and `src/frontend` for the Next.js application, along with shared `models` and `services`.

```
.
├── src/
│   ├── backend/               # FastAPI backend application
│   │   ├── routers/           # API endpoints (auth, tasks)
│   │   ├── models.py          # Database models (User, Task)
│   │   ├── schemas.py         # Request/Response data validation schemas
│   │   ├── main.py            # Main FastAPI application entry point
│   │   ├── database.py        # Database connection and session management
│   │   ├── dependencies.py    # Dependency injection for FastAPI
│   │   └── security.py        # Authentication and authorization logic
│   ├── frontend/              # Next.js frontend application
│   │   ├── src/app/           # Next.js App Router (pages and layouts)
│   │   │   ├── (auth)/        # Authentication routes (login, register)
│   │   │   ├── dashboard/     # User dashboard page
│   │   │   ├── profile/       # User profile page
│   │   │   ├── page.tsx       # Homepage
│   │   │   └── layout.tsx     # Global layout component
│   │   ├── src/components/    # Reusable React components
│   │   └── src/services/      # Frontend services for API interaction
│   ├── models/                # Shared data models (e.g., task.py)
│   └── services/              # Shared business logic services (e.g., task_manager.py)
└── pyproject.toml             # Project-level Python dependencies and configurations
```

## Getting Started

Follow these instructions to set up and run the application locally.

### Prerequisites

*   Python 3.10+
*   Node.js (LTS recommended)
*   npm or yarn
*   Poetry (for Python dependency management)
*   PostgreSQL database instance

### 1. Clone the repository

```bash
git clone https://github.com/Aashra55/Evolution-of-Todo-App-Hackathon/tree/main/Phase-II-Todo-Full-Stack-Web-Application
cd todo-web-app
```

### 2. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd src/backend
poetry install
```

#### Database Configuration

Create a `.env` file in `src/backend` with your PostgreSQL database URL:

```
DATABASE_URL="postgresql://user:password@host:port/database_name"
SECRET_KEY="your-super-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Run Database Migrations

```bash
poetry run alembic upgrade head
```

#### Start the Backend Server

```bash
poetry run uvicorn main:app --reload
```
The backend server will typically run on `http://127.0.0.1:8000`.

### 3. Frontend Setup

Open a new terminal, navigate to the frontend directory, and install dependencies:

```bash
cd src/frontend
npm install # or yarn install
```

#### Start the Frontend Development Server

```bash
npm run dev # or yarn dev
```
The frontend application will typically run on `http://localhost:3000`.

## Contributing

Feel free to open issues or submit pull requests.

## License

[MIT License](LICENSE) (placeholder, create LICENSE file if applicable)
