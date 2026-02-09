# CLI Todo App

A simple command-line todo application that stores tasks in memory.

## Features

- Add new tasks
- List all tasks
- Update task descriptions
- Mark tasks as complete
- Mark tasks as incomplete
- Remove tasks by ID

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/cli-todo-app.git
    cd cli-todo-app
    ```
    (Replace `https://github.com/your-username/cli-todo-app.git` with your actual repository URL)

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    -   **macOS/Linux:**
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