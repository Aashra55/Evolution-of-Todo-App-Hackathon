# Data Model: Todo AI Chatbot (Phase III – Basic Level)

**Date**: 2026-02-07

## Entities

### Todo

Represents a single todo item managed by the system.

*   **id**: Unique identifier (UUID). Primary key.
*   **user_id**: Identifier of the user who owns the todo. Foreign key to User entity (implicit, as User entity is not explicitly defined in basic spec but assumed by auth).
*   **description**: Text detailing the todo item. String, required.
*   **status**: Current state of the todo. String, enum: `pending`, `completed`, `deferred`. Required, default `pending`.
*   **created_at**: Timestamp of creation. Datetime, required.
*   **updated_at**: Timestamp of last update. Datetime, required.
*   **due_date**: Optional timestamp for when the todo is due. Datetime, nullable.

## Relationships

*   **Todo to User**: Many-to-one relationship. Multiple `Todo` items can belong to one `User`.

## Validation Rules

*   **description**: Must not be empty. Maximum length (e.g., 255 characters).
*   **user_id**: Must reference an existing and valid user.
*   **status**: Must be one of `pending`, `completed`, `deferred`.
*   **due_date**: If provided, must be a future date.

## State Transitions (for Todo.status)

*   `pending` → `completed`
*   `pending` → `deferred`
*   `completed` → `pending` (reopen)

## Constraints

*   **Ownership**: A `Todo` item is owned by a single `User`. Operations on a `Todo` are restricted to its owner.
*   **Data Consistency**: Strong consistency required for CRUD operations on `Todo` items.
