# Tasks: AI-powered Todo Chatbot

**Input**: Design documents from `/specs/001-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create root project directories: `backend/`, `frontend/`, `specs/001-todo-ai-chatbot/`
- [X] T002 Initialize Python backend project with Poetry: `backend/`
- [X] T003 [P] Initialize Node.js frontend project: `frontend/`
- [X] T004 Create base Dockerfile for backend application: `backend/Dockerfile`
- [X] T005 [P] Setup `.gitignore` for root, `backend/` and `frontend/` directories
- [X] T006 Configure basic logging for backend: `backend/src/config/logging.py`
- [ ] T007 Configure basic logging for frontend (if applicable): `frontend/src/config/logging.js` (or similar)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Setup database connection configuration: `backend/src/config/database.py` (or similar)
- [ ] T009 Initialize Alembic for database migrations: `backend/alembic/`
- [ ] T010 Implement base User model with Better Auth integration: `backend/src/models/user.py`
- [ ] T011 Implement Authentication dependencies for FastAPI: `backend/src/api/dependencies.py`
- [ ] T012 Implement main FastAPI application instance: `backend/src/main.py`
- [ ] T013 Create MCP Server base structure: `backend/src/mcp_server.py`
- [ ] T014 Implement base MCP Tool Handler: `backend/src/agents/tool_handler.py`
- [ ] T015 Implement main AI Agent logic: `backend/src/agents/main_agent.py`
- [ ] T016 Create base `openapi.yaml` for FastAPI: `backend/src/api/openapi.yaml` (copy from `specs/001-todo-ai-chatbot/contracts/openapi.yaml` and refine)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a Todo Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo tasks via natural language commands.

**Independent Test**: Send a natural language command to add a task (e.g., "Add a new task: Buy groceries") and verify the chatbot confirms task creation and the task appears in the Task List Panel.

### Implementation for User Story 1

- [ ] T017 [P] [US1] Implement Task model (`id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at`): `backend/src/models/todo.py`
- [ ] T018 [P] [US1] Implement Conversation model (`id`, `user_id`, `created_at`, `updated_at`): `backend/src/models/conversation.py`
- [ ] T019 [P] [US1] Implement Message model (`id`, `conversation_id`, `user_id`, `role`, `content`, `created_at`): `backend/src/models/message.py`
- [ ] T020 [P] [US1] Create database migration for Task, Conversation, Message models: `backend/alembic/versions/`
- [ ] T021 [P] [US1] Implement `add_task` MCP tool: `backend/src/mcp_tools/todo.py`
- [ ] T022 [US1] Implement a service to interact with Task, Conversation, Message models: `backend/src/services/conversation_service.py`
- [ ] T023 [US1] Update AI Agent to recognize "add task" commands and invoke `add_task` MCP tool: `backend/src/agents/main_agent.py`
- [ ] T024 [US1] Implement `POST /api/{user_id}/chat` endpoint to handle incoming chat messages and invoke AI Agent: `backend/src/api/endpoints/chat.py`
- [ ] T025 [P] [US1] Develop frontend Chat Input Box component: `frontend/src/components/ChatInput.js`
- [ ] T026 [P] [US1] Develop frontend Chat Display Area component to show messages: `frontend/src/components/ChatDisplay.js`
- [ ] T027 [US1] Integrate Chat Input and Display components with `POST /api/{user_id}/chat` endpoint: `frontend/src/pages/chat.js`
- [ ] T028 [US1] Implement frontend logic to display AI's confirmation messages and reflect task creation.

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todo Tasks (Priority: P1)

**Goal**: Enable users to see their current pending or completed todo tasks.

**Independent Test**: Send a natural language command to list tasks (e.g., "List all my pending tasks") and verify the chatbot displays the correct list and the Task List Panel updates.

### Implementation for User Story 2

- [ ] T029 [P] [US2] Implement `list_tasks` MCP tool: `backend/src/mcp_tools/todo.py`
- [ ] T030 [US2] Update AI Agent to recognize "list tasks" commands and invoke `list_tasks` MCP tool: `backend/src/agents/main_agent.py`
- [ ] T031 [P] [US2] Develop frontend Task List Panel component to display tasks: `frontend/src/components/TaskListPanel.js`
- [ ] T032 [US2] Integrate Task List Panel with backend API to fetch and display tasks: `frontend/src/pages/chat.js`
- [ ] T033 [US2] Implement frontend logic to update Task List Panel based on AI Agent's `tool_calls` response from `list_tasks`.

**Checkpoint**: User Story 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark a Task as Complete (Priority: P1)

**Goal**: Enable users to mark a task as completed once it's done.

**Independent Test**: Send a natural language command to complete a task (e.g., "Complete the task 'Buy groceries'") and observe its status change in the Task List Panel and chatbot confirmation.

### Implementation for User Story 3

- [ ] T034 [P] [US3] Implement `complete_task` MCP tool: `backend/src/mcp_tools/todo.py`
- [ ] T035 [US3] Update AI Agent to recognize "complete task" commands and invoke `complete_task` MCP tool: `backend/src/agents/main_agent.py`
- [ ] T036 [US3] Implement frontend logic to reflect task completion status in Task List Panel.
- [ ] T037 [P] [US3] Add "Mark Complete" action button logic to frontend Task List Panel: `frontend/src/components/TaskListPanel.js`

**Checkpoint**: All P1 user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete a Task (Priority: P2)

**Goal**: Enable users to remove a task from their list, with confirmation.

**Independent Test**: Send a natural language command to delete a task (e.g., "Delete the task about calling the bank"), confirm the deletion, and verify its removal from the Task List Panel.

### Implementation for User Story 4

- [ ] T038 [P] [US4] Implement `delete_task` MCP tool: `backend/src/mcp_tools/todo.py`
- [ ] T039 [US4] Update AI Agent to recognize "delete task" commands and invoke `delete_task` MCP tool, including confirmation dialogue: `backend/src/agents/main_agent.py`
- [ ] T040 [US4] Implement frontend logic to handle confirmation prompts and task removal from Task List Panel.
- [ ] T041 [P] [US4] Add "Delete" action button logic to frontend Task List Panel: `frontend/src/components/TaskListPanel.js`

**Checkpoint**: User Story 1, 2, 3, and 4 should be independently functional

---

## Phase 7: User Story 5 - Update a Task (Priority: P2)

**Goal**: Enable users to modify the title or description of an existing task.

**Independent Test**: Send a natural language command to update a task (e.g., "Update task 'Write report' to 'Finalize Q3 report'") and verify the changes in the Task List Panel.

### Implementation for User Story 5

- [ ] T042 [P] [US5] Implement `update_task` MCP tool: `backend/src/mcp_tools/todo.py`
- [ ] T043 [US5] Update AI Agent to recognize "update task" commands and invoke `update_task` MCP tool: `backend/src/agents/main_agent.py`
- [ ] T044 [US5] Implement frontend logic to reflect task updates in Task List Panel.
- [ ] T045 [P] [US5] Add "Edit" action button logic to frontend Task List Panel: `frontend/src/components/TaskListPanel.js`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T046 Refine AI Agent's natural language understanding and response generation: `backend/src/agents/main_agent.py`
- [ ] T047 Implement graceful error handling (e.g., for non-existent tasks, ambiguous commands) across backend and frontend.
- [ ] T048 [P] Implement frontend notifications/toasts for confirmations and errors.
- [ ] T049 [P] Ensure responsive design for desktop & mobile in frontend: `frontend/src/styles/global.css` (or similar)
- [ ] T050 [P] Review and apply accessible colors and fonts in frontend: `frontend/src/styles/theme.js` (or similar)
- [ ] T051 Create comprehensive `README.md` with setup instructions, usage, and deployment notes.
- [ ] T052 Finalize deployment configuration for backend and frontend.
- [ ] T053 Run `quickstart.md` validation and update as needed.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion.
  - User Stories are prioritized: P1 stories (Add, View, Complete) followed by P2 stories (Delete, Update).
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Add)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 2 (P1 - View)**: Can start after Foundational (Phase 2) - No explicit dependencies, but benefits from US1 existing tasks.
- **User Story 3 (P1 - Complete)**: Can start after Foundational (Phase 2) - No explicit dependencies, but benefits from US1 existing tasks.
- **User Story 4 (P2 - Delete)**: Can start after Foundational (Phase 2) - No explicit dependencies.
- **User Story 5 (P2 - Update)**: Can start after Foundational (Phase 2) - No explicit dependencies.

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Frontend components/integration typically depends on backend API/logic being available.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- Many tasks within each user story can run in parallel (e.g., frontend and backend components of a story).
- Once the Foundational phase completes, all user stories can be worked on in parallel by different team members.

---

## Parallel Example: User Story 1 (Add a Todo Task)

```bash
# Backend parallel tasks:
Task: "Implement Task model in backend/src/models/todo.py"
Task: "Implement Conversation model in backend/src/models/conversation.py"
Task: "Implement Message model in backend/src/models/message.py"
Task: "Implement `add_task` MCP tool in backend/src/mcp_tools/todo.py"

# Frontend parallel tasks:
Task: "Develop frontend Chat Input Box component in frontend/src/components/ChatInput.js"
Task: "Develop frontend Chat Display Area component to show messages in frontend/src/components/ChatDisplay.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Add User Story 4 → Test independently → Deploy/Demo
6.  Add User Story 5 → Test independently → Deploy/Demo
7.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    *   Developer A: User Story 1 (Add Task)
    *   Developer B: User Story 2 (View Tasks)
    *   Developer C: User Story 3 (Complete Task)
    *   Developer D: User Story 4 (Delete Task)
    *   Developer E: User Story 5 (Update Task)
3.  Stories complete and integrate independently

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
