# CLI Todo App

A simple command-line todo application that stores tasks in memory.

## Features

- Add new tasks
- List all tasks
- Update task descriptions
- Mark tasks as complete
- Mark tasks as incomplete
- Remove tasks by ID

## Tech Stack

-   **Language**: Python
-   **Runtime Dependencies**: None (pure Python standard library)
-   **Development/Testing Dependencies**: `pytest` for testing, `flake8` for linting.
-   **Application Type**: Command-Line Interface (CLI)

## Project Structure

-   `src/`: Contains the core application source code.
    -   `cli/`: Command-line interface entry point (`main.py`).
    -   `models/`: Data models for the application (e.g., `task.py`).
    -   `services/`: Business logic and core functionalities (e.g., `task_manager.py`).
-   `tests/`: Contains automated tests for the application.
    -   `integration/`: Integration tests that verify interactions between different components.
    -   `unit/`: Unit tests for individual functions and classes.
-   `.venv/`: Python virtual environment for managing dependencies.
-   `.gemini/`, `.specify/`: Configuration and scripts for the Gemini CLI agent.
-   `history/`, `specs/`: Directories related to Spec-Driven Development (SDD) artifacts.
-   `pyproject.toml`: Project configuration for Python.
-   `README.md`: Project overview and documentation.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Aashra55/Evolution-of-Todo-App-Hackathon/tree/main/Phase-I-Todo-In-Memory-Python-Console-App
    cd cli-todo-app
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    -   **Windows (PowerShell):**
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```
    -   **macOS/Linux (Bash/Zsh):**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies (for development/testing):**
    ```bash
    pip install pytest flake8
    ```
    (The app itself has no external runtime dependencies.)

## Usage (Interactive Mode)

Make sure your virtual environment is activated.

To start the interactive todo application, run:
```bash
python -m src.cli.main
```

Once inside the application, you can use the following commands:

-   **`add <description>`**: Add a new task.
    Example: `add Buy groceries`
-   **`list`**: List all tasks with their status and ID.
-   **`update <id> <new_description>`**: Update the description of a task.
    Example: `update 1 Buy organic groceries`
-   **`complete <id>`**: Mark a task as complete.
    Example: `complete 1`
-   **`incomplete <id>`**: Mark a task as incomplete (active).
    Example: `incomplete 1`
-   **`remove <id>`**: Remove a task by its ID.
    Example: `remove 1`
-   **`help`**: Display available commands.
-   **`exit`**: Exit the application.

## Running Tests

Activate your virtual environment and run:
```bash
pytest
```

## Contributing

Feel free to open issues or submit pull requests.

## License

[MIT License](LICENSE) (placeholder, create LICENSE file if applicable)