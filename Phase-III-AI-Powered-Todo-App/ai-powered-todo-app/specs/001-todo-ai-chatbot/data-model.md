# Data Model: AI-powered Todo Chatbot

**Date**: 2026-02-09
**Feature**: [./specs/001-todo-ai-chatbot/spec.md](./specs/001-todo-ai-chatbot/spec.md)

## Summary

This document defines the core data models for the AI-powered Todo Chatbot application. These models are designed to be persisted in Neon Serverless PostgreSQL using the SQLModel ORM, ensuring data integrity and alignment with application requirements.

## Entities

### Task

Represents a single todo item managed by a user.

| Field          | Type     | Description                                     | Constraints       |
| :------------- | :------- | :---------------------------------------------- | :---------------- |
| `user_id`      | `UUID`   | Identifier for the user who owns the task.      | Foreign Key (User) |
| `id`           | `UUID`   | Unique identifier for the task.                 | Primary Key, Unique |
| `title`        | `String` | Title or short description of the task.         | Not Null, Max Length: 255 |
| `description`  | `String` | Optional detailed description of the task.      | Nullable, Max Length: 1024 |
| `completed`    | `Boolean`| True if the task is completed, false otherwise. | Not Null, Default: False |
| `created_at`   | `DateTime`| Timestamp when the task was created.           | Not Null, Auto-generated |
| `updated_at`   | `DateTime`| Timestamp of the last update to the task.      | Not Null, Auto-updated |

### Conversation

Represents a chat session between a user and the AI chatbot.

| Field          | Type     | Description                                     | Constraints       |
| :------------- | :------- | :---------------------------------------------- | :---------------- |
| `user_id`      | `UUID`   | Identifier for the user involved in the conversation. | Foreign Key (User) |
| `id`           | `UUID`   | Unique identifier for the conversation.         | Primary Key, Unique |
| `created_at`   | `DateTime`| Timestamp when the conversation was initiated. | Not Null, Auto-generated |
| `updated_at`   | `DateTime`| Timestamp of the last update to the conversation. | Not Null, Auto-updated |

### Message

Represents a single message within a conversation.

| Field           | Type     | Description                                     | Constraints           |
| :-------------- | :------- | :---------------------------------------------- | :-------------------- |
| `user_id`       | `UUID`   | Identifier for the user who sent/received the message. | Foreign Key (User)    |
| `id`            | `UUID`   | Unique identifier for the message.              | Primary Key, Unique   |
| `conversation_id`| `UUID`   | Foreign key linking to the Conversation model. | Not Null, Foreign Key (Conversation) |
| `role`          | `String` | Role of the message sender (e.g., "user", "assistant", "tool"). | Not Null, Enum: ["user", "assistant", "tool"] |
| `content`       | `String` | The actual text content of the message.         | Not Null, Max Length: 4096 (arbitrary for now) |
| `created_at`    | `DateTime`| Timestamp when the message was created.        | Not Null, Auto-generated |

## Relationships

*   **User to Task:** One-to-many. A user can have multiple tasks.
*   **User to Conversation:** One-to-many. A user can have multiple conversations.
*   **Conversation to Message:** One-to-many. A conversation can have multiple messages.
*   **User to Message:** One-to-many. A user can send/receive multiple messages.
