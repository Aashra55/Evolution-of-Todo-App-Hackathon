# Data Model: Todo AI Chatbot Phase V

This document outlines the conceptual data model for the Todo AI Chatbot Phase V, focusing on entities, their attributes, and relationships. It is technology-agnostic and defines the logical structure of data managed by the system.

## Entities

### 1. Task

Represents a single todo item managed by a user.

-   **Fields**:
    -   `id` (UUID/String): Unique identifier for the task.
    -   `title` (String): A brief description of the task.
    -   `description` (String, Optional): A more detailed description of the task.
    -   `status` (Enum: "pending", "completed", "in_progress", "cancelled"): Current state of the task.
    -   `priority` (Enum: "low", "medium", "high", "urgent"): Importance level of the task.
    -   `tags` (Array of Strings): Categorization labels for the task.
    -   `dueDate` (Timestamp, Optional): The date and time by which the task is expected to be completed.
    -   `reminderSettings` (Object, Optional): Configuration for task reminders.
        -   `remindAt` (Timestamp): The specific time a reminder should be triggered.
        -   `channel` (Enum: "chat", "email", "app_notification"): Preferred notification channel.
        -   `status` (Enum: "scheduled", "sent", "failed"): Status of the reminder notification.
    -   `recurrencePattern` (Object, Optional): Defines if and how a task recurs.
        -   `type` (Enum: "daily", "weekly", "monthly", "yearly", "custom"): Type of recurrence.
        -   `interval` (Integer, Optional): E.g., every `N` days/weeks.
        -   `daysOfWeek` (Array of Strings, Optional): E.g., ["MON", "WED"] for weekly.
        -   `dayOfMonth` (Integer, Optional): E.g., 15 for monthly.
        -   `endDate` (Timestamp, Optional): When the recurrence should stop.
    -   `userId` (UUID/String): Identifier of the user who owns the task.
    -   `createdAt` (Timestamp): Timestamp when the task was created.
    -   `updatedAt` (Timestamp): Last timestamp when the task was modified.

-   **Relationships**:
    -   `belongs_to` a User (via `userId`).

### 2. User

Represents a user of the Todo AI Chatbot.

-   **Fields**:
    -   `id` (UUID/String): Unique identifier for the user.
    -   `username` (String): User's unique username.
    -   `email` (String): User's email address for notifications.
    -   `notificationPreferences` (Object, Optional): User-specific settings for receiving notifications.
        -   `channels` (Array of Enums: "chat", "email", "app_notification"): Preferred notification channels.
        -   `doNotDisturb` (Boolean): Flag to suppress notifications.
        -   `locale` (String): User's preferred language/locale for notifications.

-   **Relationships**:
    -   `owns` multiple Tasks.

### 3. Conversation State

Represents transient state for ongoing chat interactions, crucial for AI context and conversational continuity. Managed by Dapr State Store.

-   **Fields**:
    -   `userId` (UUID/String): Identifier of the user associated with the conversation.
    -   `context` (JSON Object): Stores AI context, current conversational topic, last recognized intent, etc.
    -   `lastInteractionTimestamp` (Timestamp): The last time the user interacted with the chatbot in this conversation.
    -   `sessionId` (UUID/String): Identifier for the current conversational session.

-   **Relationships**:
    -   `associated_with` a User (via `userId`).

### 4. Event

Represents a system or user action. Events are immutable records of facts that have occurred.

-   **Fields**:
    -   `eventId` (UUID/String): Unique identifier for the event.
    -   `eventType` (String): Type of event (e.g., "TaskCreated", "TaskUpdated", "ReminderSent", "TaskRecurrenceGenerated").
    -   `sourceService` (String): The service that produced the event.
    -   `timestamp` (Timestamp): When the event occurred.
    -   `payload` (JSON Object): Detailed data related to the event (e.g., full Task object for "TaskCreated", diff for "TaskUpdated").
    -   `correlationId` (UUID/String, Optional): Used to link related events across different services or actions.
    -   `userId` (UUID/String, Optional): The user who initiated the action, if applicable.

-   **Relationships**:
    -   `can_relate_to` a Task (via `payload.taskId` or `payload.task_data.id`).
    -   `can_relate_to` a User (via `userId`).

## Data Flow & Storage Responsibility

-   **PostgreSQL**: Primarily stores `Task` and `User` entities. This is the source of truth for long-lived, business-critical data.
-   **Dapr State Store**: Primarily stores `Conversation State`. Can also be used for transient per-service states or caches where eventual consistency is acceptable.
-   **Kafka Topics**: Events are streamed through Kafka topics (`task-events`, `reminders`, `task-updates`). These topics are for inter-service communication and can serve as a basis for an event log.
-   **Audit Log Service**: Consumes relevant events and stores them for audit/historical purposes (storage mechanism for audit logs to be determined, likely a specialized log store or a separate DB optimized for append-only data).