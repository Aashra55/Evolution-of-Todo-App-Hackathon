# Data Model: AI-powered Todo Chatbot

This document defines the core data entities and their attributes for the AI-powered Todo Chatbot, aligning with the project's requirement to store tasks, conversations, and messages persistently using Neon Serverless PostgreSQL and SQLModel.

## Core Entities

All models are designed for use with SQLModel for ORM, inheriting from `SQLModel`.

### Task Model

Represents a single todo item managed by a user.

| Field        | Type        | Constraints      | Description                                     |
| :----------- | :---------- | :--------------- | :---------------------------------------------- |
| `user_id`    | `UUID`      | Primary Key Part | Identifier for the user who owns the task.      |
| `id`         | `UUID`      | Primary Key Part | Unique identifier for the task.                 |
| `title`      | `String`    | Not Null         | Title or short description of the task.         |
| `description`| `Optional[String]`| Nullable     | Optional detailed description of the task.      |
| `completed`  | `Boolean`   | Not Null, Default: `False` | True if the task is completed, false otherwise. |
| `created_at` | `DateTime`  | Not Null         | Timestamp when the task was created.            |
| `updated_at` | `DateTime`  | Not Null         | Timestamp of the last update to the task.       |

**Relationships:**
*   A `User` can have multiple `Task`s. (Implicit, `user_id` serves as a foreign key).

**Validation Rules (Conceptual):**
*   `title` should not be empty.
*   `title` length should be reasonable (e.g., max 255 characters).

### Conversation Model

Represents a chat session between a user and the AI chatbot.

| Field        | Type        | Constraints      | Description                                     |
| :----------- | :---------- | :--------------- | :---------------------------------------------- |
| `user_id`    | `UUID`      | Primary Key Part | Identifier for the user involved in the conversation. |
| `id`         | `UUID`      | Primary Key Part | Unique identifier for the conversation.         |
| `created_at` | `DateTime`  | Not Null         | Timestamp when the conversation was initiated.  |
| `updated_at` | `DateTime`  | Not Null         | Timestamp of the last update to the conversation. |

**Relationships:**
*   A `User` can have multiple `Conversation`s. (Implicit, `user_id` serves as a foreign key).
*   A `Conversation` can have multiple `Message`s.

### Message Model

Represents a single message within a conversation.

| Field            | Type        | Constraints      | Description                                     |
| :--------------- | :---------- | :--------------- | :---------------------------------------------- |
| `user_id`        | `UUID`      | Foreign Key      | Identifier for the user who sent/received the message. |
| `id`             | `UUID`      | Primary Key      | Unique identifier for the message.              |
| `conversation_id`| `UUID`      | Foreign Key      | Foreign key linking to the `Conversation` model. |
| `role`           | `String`    | Not Null         | Role of the message sender (e.g., "user", "assistant", "tool"). |
| `content`        | `String`    | Not Null         | The actual text content of the message.         |
| `created_at`     | `DateTime`  | Not Null         | Timestamp when the message was created.         |

**Relationships:**
*   A `Conversation` can have multiple `Message`s. (`conversation_id` serves as a foreign key).

## Relationships Overview

*   **User to Task:** One-to-Many. A user can create and manage many tasks.
*   **User to Conversation:** One-to-Many. A user can have multiple chat conversations.
*   **Conversation to Message:** One-to-Many. Each conversation consists of multiple messages.
*   **Message to User/Conversation:** Many-to-One. Each message belongs to one user and one conversation.