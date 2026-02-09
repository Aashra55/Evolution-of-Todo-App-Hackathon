# API Contracts: Todo AI Chatbot (Phase III – Basic Level)

**Date**: 2026-02-07

## Backend Endpoints

All endpoints require authentication via Better Auth tokens unless explicitly stated otherwise. Error responses will be consistent across the API, providing clear error codes and messages without exposing internal server details.

### Chat Endpoint

*   **Endpoint**: `/chat`
*   **Method**: `POST`
*   **Description**: Handles incoming user messages and returns chatbot responses. This endpoint processes conversational input, forwards it to the AI agent via MCP, and returns the agent's natural language response.
*   **Request Body**:
    ```json
    {
      "message": "string",
      "conversation_id": "string (UUID, optional for new conversation)"
    }
    ```
*   **Response Body (Success)**:
    ```json
    {
      "reply": "string",
      "conversation_id": "string (UUID)"
    }
    ```
*   **Response Body (Error)**: (Consistent error structure across API)
    ```json
    {
      "error": {
        "code": "string",
        "message": "string",
        "details": "object (optional)"
      }
    }
    ```

### Create Todo

*   **Endpoint**: `/todos`
*   **Method**: `POST`
*   **Description**: Creates a new todo item for the authenticated user.
*   **Request Body**:
    ```json
    {
      "description": "string",
      "due_date": "string (ISO 8601, optional)"
    }
    ```
*   **Response Body (Success)**:
    ```json
    {
      "id": "string (UUID)",
      "description": "string",
      "status": "string (e.g., pending)",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "due_date": "string (ISO 8601, optional)"
    }
    ```

### Retrieve, Update, or Delete Specific Todo

*   **Endpoint**: `/todos/{todo_id}`
*   **Method**: `GET`, `PUT`, `DELETE`
*   **Description**:
    *   `GET`: Retrieves a specific todo item by ID for the authenticated user.
    *   `PUT`: Updates an existing todo item by ID for the authenticated user.
    *   `DELETE`: Deletes a specific todo item by ID for the authenticated user.
*   **Path Parameters**:
    *   `todo_id`: string (UUID) - The ID of the todo item.
*   **Request Body (`PUT` only)**:
    ```json
    {
      "description": "string (optional)",
      "status": "string (e.g., completed, deferred, pending, optional)",
      "due_date": "string (ISO 8601, optional)"
    }
    ```
*   **Response Body (GET/PUT Success)**: (Same as Create Todo success response)
    ```json
    {
      "id": "string (UUID)",
      "description": "string",
      "status": "string",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "due_date": "string (ISO 8601, optional)"
    }
    ```
*   **Response Body (DELETE Success)**: (Empty or confirmation message)
    ```json
    {
      "message": "Todo deleted successfully"
    }
    ```

### List Todos for User

*   **Endpoint**: `/todos/user/{user_id}`
*   **Method**: `GET`
*   **Description**: Lists all todo items for a specific authenticated user.
*   **Path Parameters**:
    *   `user_id`: string (UUID) - The ID of the user. (Note: In practice, user_id would often be derived from the authenticated context, but spec implies it might be explicit)
*   **Response Body (Success)**:
    ```json
    [
      {
        "id": "string (UUID)",
        "description": "string",
        "status": "string",
        "created_at": "string (ISO 8601)",
        "updated_at": "string (ISO 8601)",
        "due_date": "string (ISO 8601, optional)"
      }
      // ... more todo items
    ]
    ```
