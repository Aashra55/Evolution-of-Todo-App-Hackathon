<!--
Sync Impact Report:
Version change: Initial -> 1.0.0
Modified principles: None (initial creation)
Added sections:
  - I. Agentic Development Workflow
  - II. Stateless and Scalable Architecture
  - III. MCP Tools as Primary Interface
  - IV. Structured Data Model & Persistence
  - V. Clear API Contracts
  - VI. Operational Readiness
  - Project Components and Responsibilities
  - Architectural Overview
  - Database Models
  - API Endpoints
  - MCP Tools
  - Agent Behavior and Conversation Flow
  - Natural Language Commands (Examples)
  - Deployment Notes
  - Deliverables
Removed sections: None (initial creation)
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .gemini/commands/sp.adr.toml ⚠ pending
  - .gemini/commands/sp.analyze.toml ⚠ pending
  - .gemini/commands/sp.checklist.toml ⚠ pending
  - .gemini/commands/sp.clarify.toml ⚠ pending
  - .gemini/commands/sp.constitution.toml ⚠ pending
  - .gemini/commands/sp.git.commit_pr.toml ⚠ pending
  - .gemini/commands/sp.implement.toml ⚠ pending
  - .gemini/commands/sp.phr.toml ⚠ pending
  - .gemini/commands/sp.plan.toml ⚠ pending
  - .gemini/commands/sp.reverse-engineer.toml ⚠ pending
  - .gemini/commands/sp.specify.toml ⚠ pending
  - .gemini/commands/sp.tasks.toml ⚠ pending
  - .gemini/commands/sp.taskstoissues.toml ⚠ pending
Follow-up TODOs: Ensure `plan-template.md`, `spec-template.md`, `tasks-template.md` and command files are updated to align with the new constitution.
-->
# Phase III: Todo AI Chatbot Constitution

## Core Principles

### I. Agentic Development Workflow
Every feature and system component shall strictly follow the Agentic Development Stack workflow: Specification → Planning → Tasks → Implementation. This ensures a structured, testable, and verifiable development process. All work must be guided by clear specs, detailed plans, atomic tasks, and robust implementations.

### II. Stateless and Scalable Architecture
The system architecture shall prioritize stateless server components, ensuring horizontal deployability and scalability. Persistence will be managed exclusively through the database. This principle enables robust, fault-tolerant, and elastic scaling of compute resources independently of data storage.

### III. MCP Tools as Primary Interface
All core business logic and task operations shall be exposed and managed through the Official MCP SDK, functioning as a set of callable tools. The AI Agent will interact with the system primarily by mapping natural language commands to these MCP tools, incorporating confirmations and comprehensive error handling.

### IV. Structured Data Model & Persistence
All application data, including tasks, conversations, and messages, shall adhere to clearly defined database models (Task, Conversation, Message). Data will be persisted in Neon Serverless PostgreSQL using the SQLModel ORM, ensuring data integrity, schema evolution, and efficient querying.

### V. Clear API Contracts
All external interfaces, particularly the Chat API Endpoint, shall adhere to explicit and well-documented API contracts. This includes defining request/response formats, required parameters, and error taxonomies, ensuring predictable and reliable interaction with client applications.

### VI. Operational Readiness
The system shall be designed for operational readiness from inception, including considerations for deployment, environment configuration (e.g., allowlisting, environment variables), and monitoring hooks. This ensures a smooth transition from development to production and simplifies ongoing maintenance.

## Project Components and Responsibilities

### Frontend: OpenAI ChatKit
*   **Purpose:** User interface for interacting with the AI-powered todo chatbot.
*   **Key Functionality:** Display chat history, send user messages, render AI responses, and potentially visualize tool calls.
*   **Deployment Note:** Requires domain allowlisting and `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` environment variable.

### Backend: Python FastAPI
*   **Purpose:** Expose the Chat API endpoint and orchestrate interactions between the Frontend, AI Agent, and Database.
*   **Key Functionality:** Handle HTTP requests, manage user sessions, invoke the AI Agent, and relay responses.
*   **Architecture:** Designed to be stateless and horizontally scalable.

### AI Agent: OpenAI Agents SDK
*   **Purpose:** Interpret natural language commands and execute corresponding actions via MCP Tools.
*   **Key Functionality:** Natural Language Understanding (NLU), tool selection, tool invocation, response generation, error handling, and confirmation dialogues.
*   **Behavior:** Maps user commands to `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`.

### MCP Server: Official MCP SDK
*   **Purpose:** Provides a standardized interface for core task management operations.
*   **Key Functionality:** Exposes `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task` as callable tools for the AI Agent.
*   **Benefit:** Enables consistent and testable execution of business logic, promotes tool composition.

### Database: Neon Serverless PostgreSQL (ORM: SQLModel)
*   **Purpose:** Persistent storage for all application data (Tasks, Conversations, Messages).
*   **Key Functionality:** Store, retrieve, update, and delete task and conversation-related data.
*   **Characteristic:** Serverless, highly available, scalable.

### Authentication: Better Auth
*   **Purpose:** Secure user access and ensure proper authorization for all operations.
*   **Key Functionality:** User authentication, session management, and access control for API endpoints and data.

## Architectural Overview

The system follows a layered architecture, emphasizing separation of concerns and scalability.

```
+----------------+       +-------------------+       +--------------------+
|                |       |                   |       |                    |
|  User (Client) | <---> | Frontend (ChatKit)| <---> | Backend (FastAPI)  |
|                |       |                   |       | (Stateless Server) |
+----------------+       +-------------------+       +--------------------+
                                      ^
                                      |
                                      v
                             +-------------------+
                             |                   |
                             | AI Agent          |
                             | (OpenAI Agents SDK)|
                             +-------------------+
                                      ^
                                      | Maps NL to Tools
                                      v
                             +-------------------+
                             |                   |
                             | MCP Server        |
                             | (Official MCP SDK)|
                             | (Task Operations) |
                             +-------------------+
                                      ^
                                      | Persists Data / Retrieves Data
                                      v
                             +-------------------+
                             |                   |
                             | Database          |
                             | (Neon Serverless  |
                             |  PostgreSQL)      |
                             +-------------------+
```

**Flow:**
1.  **User Input:** User interacts with the Frontend (OpenAI ChatKit) via natural language.
2.  **Frontend to Backend:** User message is sent to the Backend (FastAPI) Chat API endpoint.
3.  **Backend to AI Agent:** Backend fetches conversation history from the Database, builds a message array, and passes it to the AI Agent.
4.  **AI Agent to MCP Server:** AI Agent interprets the natural language command, selects the appropriate MCP tool (e.g., `add_task`), and invokes it through the MCP Server.
5.  **MCP Server to Database:** MCP Tool executes its logic, interacting with the Database (e.g., creating a new task record).
6.  **Database to MCP Server:** Database returns results of the operation.
7.  **MCP Server to AI Agent:** MCP Server returns tool call results to the AI Agent.
8.  **AI Agent to Backend:** AI Agent processes tool results, generates a natural language response, and optionally provides tool call details.
9.  **Backend to Frontend:** Backend stores the new user message and AI response in the Database and returns the response to the Frontend.
10. **Frontend to User:** Frontend displays the AI's response to the user.

## Database Models

All models use SQLModel for ORM.

### Task Model
| Field        | Type      | Description                                |
| :----------- | :-------- | :----------------------------------------- |
| `user_id`    | `UUID`    | Identifier for the user who owns the task. |
| `id`         | `UUID`    | Unique identifier for the task.            |
| `title`      | `String`  | Title or short description of the task.    |
| `description`| `String`  | Optional detailed description of the task. |
| `completed`  | `Boolean` | True if the task is completed, false otherwise. |
| `created_at` | `DateTime`| Timestamp when the task was created.       |
| `updated_at` | `DateTime`| Timestamp of the last update to the task.  |

### Conversation Model
| Field        | Type      | Description                                |
| :----------- | :-------- | :----------------------------------------- |
| `user_id`    | `UUID`    | Identifier for the user involved in the conversation. |
| `id`         | `UUID`    | Unique identifier for the conversation.    |
| `created_at` | `DateTime`| Timestamp when the conversation was initiated. |
| `updated_at` | `DateTime`| Timestamp of the last update to the conversation. |

### Message Model
| Field            | Type      | Description                                |
| :--------------- | :-------- | :----------------------------------------- |
| `user_id`        | `UUID`    | Identifier for the user who sent/received the message. |
| `id`             | `UUID`    | Unique identifier for the message.         |
| `conversation_id`| `UUID`    | Foreign key linking to the Conversation model. |
| `role`           | `String`  | Role of the message sender (e.g., "user", "assistant", "tool"). |
| `content`        | `String`  | The actual text content of the message.    |
| `created_at`     | `DateTime`| Timestamp when the message was created.    |

## API Endpoints

### Chat API Endpoint
**Path:** `POST /api/{user_id}/chat`
**Description:** Main endpoint for user interaction with the AI chatbot.

| Parameter         | Type           | Description                                        | Required |
| :---------------- | :------------- | :------------------------------------------------- | :------- |
| **Request Body:** |                |                                                    |          |
| `conversation_id` | `UUID` (query) | Optional: ID of an existing conversation. If omitted, a new one is started. | No       |
| `message`         | `String`       | Required: The user's natural language message.     | Yes      |
| **Response Body:**|                |                                                    |          |
| `conversation_id` | `UUID`         | ID of the conversation.                            | Yes       |
| `response`        | `String`       | AI Agent's natural language reply.                 | Yes       |
| `tool_calls`      | `List[Object]` | Optional: Details of any tool calls made by the agent. | No       |

## MCP Tools

These tools are exposed by the MCP Server and are callable by the AI Agent.

| Tool Name     | Description                                        | Signature (Conceptual)                          |
| :------------ | :------------------------------------------------- | :---------------------------------------------- |
| `add_task`    | Creates a new todo task.                           | `add_task(user_id: UUID, title: str, description: Optional[str])` |
| `list_tasks`  | Retrieves a list of todo tasks for a user.         | `list_tasks(user_id: UUID, completed: Optional[bool])` |
| `complete_task`| Marks a specific task as completed.                | `complete_task(user_id: UUID, task_id: UUID)`   |
| `delete_task` | Deletes a specific task.                           | `delete_task(user_id: UUID, task_id: UUID)`     |
| `update_task` | Modifies an existing task's title or description.  | `update_task(user_id: UUID, task_id: UUID, title: Optional[str], description: Optional[str], completed: Optional[bool])` |

**Tool Composition Benefits:**
By formalizing task operations as discrete, callable MCP tools, the system gains significant advantages:
*   **Modularity:** Each tool encapsulates a specific piece of business logic.
*   **Reusability:** Tools can be reused across different agent behaviors or even other interfaces.
*   **Testability:** Each tool can be independently tested, simplifying debugging and ensuring reliability.
*   **Extensibility:** New tools can be added or existing ones modified without impacting the core agent logic, promoting easier feature expansion.

## Agent Behavior and Conversation Flow

### Agent Behavior
The AI Agent's primary function is to accurately map natural language commands from the user to the appropriate MCP Tools.
*   **Interpretation:** Understand user intent and extract necessary parameters from natural language.
*   **Tool Selection:** Choose the correct MCP tool based on interpreted intent.
*   **Confirmation:** Engage in confirmation dialogues with the user before executing destructive or significant actions (e.g., deleting tasks).
*   **Error Handling:** Gracefully handle errors returned by MCP tools or during tool invocation, providing informative feedback to the user.
*   **Response Generation:** Generate natural language responses that confirm actions, provide requested information, or explain failures.

### Conversation Flow
The conversation flow is designed to be stateless at the server level, with conversation history managed through the database.
1.  **Incoming Message:** A new message arrives at the FastAPI `chat` endpoint.
2.  **History Retrieval:** The Backend retrieves the entire conversation history (if `conversation_id` is provided) from the Neon Serverless PostgreSQL database.
3.  **Message Array Construction:** The retrieved history, along with the current user message, is assembled into a message array suitable for the OpenAI Agents SDK.
4.  **Agent Invocation:** The AI Agent is invoked with the message array and access to the MCP Tools.
5.  **Tool Execution (if needed):** If the Agent determines a tool call is necessary, it invokes the relevant MCP Tool.
6.  **Response Handling:** The Agent processes the tool's output and generates a natural language response.
7.  **Persistence:** The new user message and the Agent's response (along with any tool call details) are stored in the database, linking to the conversation.
8.  **Client Response:** The Backend returns the Agent's response and tool call details to the Frontend.

## Natural Language Commands (Examples)

The AI Agent should be able to understand and execute commands similar to:
*   "Add a new task: Buy groceries for dinner tonight."
*   "List all my pending tasks."
*   "What do I need to do?"
*   "Complete the task 'Walk the dog'."
*   "Delete the task about calling the bank."
*   "Update task 'Write report' to 'Finalize Q3 report' and mark it as completed."
*   "Show me my completed tasks."
*   "I need to remember to call Mom tomorrow."
*   "Remove 'Go to gym'."

## Deployment Notes

*   **OpenAI ChatKit Domain Whitelisting:** The domain hosting the Frontend (OpenAI ChatKit) must be explicitly whitelisted in the OpenAI configuration to prevent unauthorized access.
*   **Environment Variables:**
    *   `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`: Required by OpenAI ChatKit for domain authentication.
    *   Database connection strings and authentication tokens for Better Auth must be secured via environment variables.
*   **Containerization:** Both Frontend and Backend components should be containerized for consistent deployment across environments.
*   **Serverless Database:** Leverage Neon Serverless PostgreSQL's auto-scaling capabilities for database resources.
*   **Scalability:** The stateless nature of the FastAPI backend allows for easy horizontal scaling of instances based on traffic load.

## Deliverables

*   **GitHub Repository Structure:** A well-organized repository containing all project code, configurations, and documentation.
*   **Feature Specifications (`specs/`):** Detailed specifications for each feature implemented.
*   **Database Migrations:** Scripts for evolving the database schema.
*   **Comprehensive README:** Clear instructions for setup, development, testing, and deployment.
*   **Working Chatbot:** A fully functional AI-powered todo chatbot, demonstrating all specified features.

## Governance
This Constitution outlines the foundational principles and architectural decisions for the "Phase III: Todo AI Chatbot" project. It serves as the single source of truth for project direction.

**Amendment Procedure:** Any proposed amendments to this Constitution must be documented, undergo a formal review process, and be approved by the project's architects and stakeholders. A migration plan outlining the impact of the change must accompany significant amendments.

**Versioning Policy:** The Constitution version shall follow Semantic Versioning (MAJOR.MINOR.PATCH).
*   **MAJOR:** Backward incompatible changes, removal of principles, or fundamental architectural shifts.
*   **MINOR:** Addition of new principles, significant expansion of guidance, or substantial structural changes.
*   **PATCH:** Clarifications, wording improvements, typo fixes, or non-semantic refinements.

**Compliance Review:** All code changes, architectural designs, and development practices must be reviewed for compliance with the principles and guidelines set forth in this Constitution. Deviations must be explicitly justified and approved.

**Version**: 1.0.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-09