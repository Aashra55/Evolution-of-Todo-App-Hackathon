# Data Model: Local Kubernetes Deployment

**Branch**: `002-local-k8s-deploy` | **Date**: 2026-02-09 | **Plan**: specs/002-local-k8s-deploy/plan.md
**Context**: Inferred data model for the "Todo Chatbot" application based on common functionality.

## Entities

### 1. User

Represents a user of the Todo Chatbot application.

-   **Attributes**:
    -   `id`: UUID (Primary Key)
    -   `username`: String (Unique, e.g., for login)
    -   `email`: String (Unique, e.g., for notifications, login)
    -   `password_hash`: String (Securely stored hash of the user's password)
    -   `created_at`: Timestamp (Record creation time)
    -   `updated_at`: Timestamp (Record last update time)
-   **Relationships**:
    -   One-to-many with `TodoItem` (A user can have multiple todo items).
-   **Validation Rules**:
    -   `username` and `email` must be unique.
    -   `email` must be a valid email format.
    -   `password_hash` must be present.

### 2. TodoItem

Represents a single task or todo item belonging to a user.

-   **Attributes**:
    -   `id`: UUID (Primary Key)
    -   `user_id`: UUID (Foreign Key to User.id)
    -   `title`: String (Brief description of the todo item)
    -   `description`: Text (Optional, detailed description)
    -   `status`: String (e.g., 'pending', 'completed', 'in progress'. Default: 'pending')
    -   `due_date`: Date (Optional, target completion date)
    -   `created_at`: Timestamp (Record creation time)
    -   `updated_at`: Timestamp (Record last update time)
-   **Relationships**:
    -   Many-to-one with `User` (A todo item belongs to one user).
-   **Validation Rules**:
    -   `title` must not be empty.
    -   `user_id` must refer to an existing `User`.
    -   `status` must be one of the predefined values.
