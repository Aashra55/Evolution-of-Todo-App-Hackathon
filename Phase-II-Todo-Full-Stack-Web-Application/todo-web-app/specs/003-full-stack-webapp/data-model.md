# Data Model

This document outlines the data models for the User and Task entities, based on the feature specification.

## Entity: User

Represents an individual with an account in the system.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-incrementing | Unique identifier for the user. |
| `email` | String | Not Null, Unique | The user's email address, used for login. |
| `hashed_password` | String | Not Null | The user's password, stored securely after hashing. |

### Relationships

- A **User** has a one-to-many relationship with the **Task** entity. One user can own many tasks.

## Entity: Task

Represents a single to-do item.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-incrementing | Unique identifier for the task. |
| `description` | String | Not Null | The text content of the to-do item. |
| `completed` | Boolean | Not Null, Default: `false` | The completion status of the task. |
| `owner_id` | Integer | Foreign Key (User.id) | A reference to the user who owns this task. |

### Relationships

- A **Task** has a many-to-one relationship with the **User** entity. Each task belongs to exactly one user.

## State Transitions (Task)

- A **Task** is created with `completed` as `false`.
- The `completed` status can be toggled between `true` and `false` through user interaction.
- The `description` can be updated at any time by the owning user.
