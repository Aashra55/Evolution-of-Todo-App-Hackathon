# Tasks: Todo AI Chatbot (Phase III – Basic Level)

**Input**: Design documents from `/specs/001-todo-ai-chatbot-basic/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: All tasks should incorporate a test-first approach where applicable.

**Organization**: Tasks are grouped by major system components/layers and logical phases.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure across all components.

- [X] T001 Create project root directories: `backend/`, `frontend/`, `ai-agent/`.
- [X] T002 Create component subdirectories: `backend/src/models`, `backend/src/services`, `backend/src/api`, `backend/tests`, `frontend/src/components`, `frontend/src/pages`, `frontend/src/services`, `frontend/tests`, `ai-agent/src/agents`, `ai-agent/tests`.
- [X] T003 Initialize Python project for backend (FastAPI, SQLModel) in `backend/` with `pyproject.toml` or `requirements.txt`.
- [X] T004 Initialize Node.js project for frontend (OpenAI ChatKit, if applicable) in `frontend/` with `package.json`.
- [X] T005 Initialize Python project for AI Agent (OpenAI Agents SDK) in `ai-agent/` with `pyproject.toml` or `requirements.txt`.
- [X] T006 [P] Configure linting and formatting (e.g., Ruff for Python, ESLint/Prettier for JS) for all components.
- [X] T007 Setup initial Git repository structure, if not already configured, and create a base README.md.

---

## Phase 2: Foundational (Backend Core - Data, Auth, API)

**Purpose**: Establish core backend services including data persistence, authentication, and the initial API.

- [X] T008 [AC-007, AC-008] Implement Todo Domain Model (SQLModel entity for `Todo` with `id`, `user_id`, `description`, `status`, `created_at`, `updated_at`, `due_date`) in `backend/src/models/todo.py`.
- [X] T009 [AC-008] Implement Database Connection and Session Management using SQLModel and Neon Serverless PostgreSQL in `backend/src/services/database.py`.
- [X] T010 [AC-007] Implement basic CRUD operations (Create, Read, Update, Delete) for the `Todo` entity in `backend/src/services/todo_service.py`.
- [X] T011 [AC-002, AC-009] Implement Authentication (Better Auth integration, token validation) middleware in `backend/src/api/auth.py` and integrate into FastAPI app.
- [X] T012 [P] [AC-009, AC-010] Implement Authorization logic (ensuring user ownership for todo operations) in `backend/src/api/dependencies.py`.
- [X] T013 [AC-008] Set up database migrations (e.g., Alembic) in `backend/migrations/`.
- [X] T014 [AC-009] Implement Backend API Endpoints (`/todos`, `/todos/{todo_id}`, `/todos/user/{user_id}`) as defined in `contracts/api.md` in `backend/src/api/endpoints/todo.py`.
- [X] T015 [AC-009] Implement consistent API Error Handling strategy in `backend/src/api/errors.py`.

---

## Phase 3: MCP Server & AI Agent Core

**Purpose**: Build the intermediary layer for AI agent interaction and the core AI logic.

- [X] T016 [AC-006] Implement MCP Server framework (Official MCP SDK integration) to host tools in `backend/src/mcp_server.py`.
- [X] T017 [AC-005, AC-006] Implement MCP Tools for Todo CRUD operations (matching `todo_service.py` functions) and expose them via the MCP Server in `backend/src/mcp_tools/todo.py`.
- [X] T018 [AC-005] Implement AI Agent Core (OpenAI Agents SDK setup, agent initialization, tool registration) in `ai-agent/src/agents/main_agent.py`.
- [X] T019 [AC-005] Integrate AI Agent with MCP Tools (configure agent's ability to call the MCP tools) in `ai-agent/src/agents/tool_handler.py`.
- [X] T020 [AC-003, AC-004] Implement conversational context persistence mechanism (e.g., storing conversation turns) in `backend/src/services/conversation_service.py`.

---

## Phase 4: Conversational Interface (Backend API & Frontend Integration)

**Purpose**: Connect the chat frontend to the AI agent via a dedicated chat endpoint.

- [X] T021 [AC-001, AC-004] Implement stateless chat endpoint `/chat` in `backend/src/api/endpoints/chat.py`. This endpoint will forward messages to the AI Agent and return its response.
- [X] T022 [P] [AC-001] Design and implement basic chat UI components (message display area, user input field, send button) in `frontend/src/components/chat/`.
- [X] T023 [P] [AC-001] Implement API client for the `/chat` endpoint in `frontend/src/services/chat_api.js`.
- [X] T024 [AC-001, AC-003] Integrate frontend chat UI with the backend `/chat` API, handling message flow, conversation ID, and displaying responses in `frontend/src/pages/chat.js`.

---

## Phase 5: UI/UX Implementation

**Purpose**: Ensure the frontend adheres to the defined UI/UX specifications.

- [X] T025 [AC-016, AC-017] Implement overall UI layout, ensuring clear visual separation between the chat interface and the todo information display (e.g., side-by-side panels) in `frontend/src/layouts/main.js`.
- [X] T026 [AC-017, AC-018] Design and implement todo list display components with consistent styling, spacing, and clear visual hierarchy in `frontend/src/components/todos/todo_list.js` and `frontend/src/components/todos/todo_item.js`.
- [X] T027 [AC-018] Ensure all interactive UI elements (buttons, input fields) have clear affordances (hover states, focus states, disabled states) through CSS styling or component logic in `frontend/src/styles/theme.css`.
- [X] T028 [AC-019] Implement UI for empty states (e.g., "No todos yet"), error messages, and loading indicators in `frontend/src/components/common/feedback_messages.js`.
- [X] T029 [AC-016, AC-017, AC-020] Conduct a comprehensive UI review to refine visual clarity, spacing, alignment, and adherence to the professional tone and visual constraints specified in `frontend/src/styles/global.css`.
- [X] T030 [AC-018] Verify repeated UI elements (e.g., individual todo cards, chat bubbles) are visually consistent in size, spacing, and styling.

---

## Phase 6: Testing & Validation

**Purpose**: Ensure all components function correctly and meet acceptance criteria.

- [X] T031 [AC-012] Implement backend unit tests for Todo domain model, services, and utility functions in `backend/tests/unit/`.
- [X] T032 [AC-012] Implement backend integration tests for API endpoints and database interaction to verify CRUD operations and authentication in `backend/tests/integration/`.
- [X] T033 [AC-005, AC-012] Implement AI Agent tests for intent recognition, tool invocation, and response generation against various natural language inputs in `ai-agent/tests/`.
- [X] T034 [P] Implement frontend unit tests for UI components (e.g., chat input, todo item) in `frontend/tests/unit/`.
- [X] T035 [AC-001, AC-002, AC-003, AC-005] Implement end-to-end tests for critical user journeys (e.g., "create todo via chat", "complete todo via chat") using a framework like Playwright or Cypress in `frontend/tests/e2e/`.
- [X] T036 [AC-016, AC-017, AC-018, AC-019, AC-020] Conduct manual UI/UX review and validation against all UI-related acceptance criteria.
- [X] T037 [AC-013] Verify basic logging is functional and captures key events for monitoring and debugging.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Address non-functional requirements and final checks before deployment.

- [X] T038 [AC-011] Implement basic scalability measures (e.g., Dockerfile for backend, AI agent, production-ready configurations) in `backend/Dockerfile`, `ai-agent/Dockerfile`.
- [X] T039 [AC-013] Implement basic observability (structured logging configuration, environment variable management for logs) in `backend/src/config/logging.py`, `ai-agent/src/config/logging.py`.
- [X] T040 [AC-014] Conduct a final review to verify strict adherence to agentic workflows for all implemented components (no manual coding).
- [X] T041 [AC-015] Conduct a final review to verify no introduction of technologies outside the mandated stack.
- [X] T042 Update `quickstart.md` with final setup instructions, API endpoints, and any specific agent configuration details.
- [X] T043 Update `GEMINI.md` to reflect any final changes in project commands or structure.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all subsequent functional phases.
- **MCP Server & AI Agent Core (Phase 3)**: Depends on Foundational phase completion. Can run in parallel with some UI development but requires backend API stability.
- **Conversational Interface (Phase 4)**: Depends on Foundational (API) and MCP/AI Agent Core (for chat endpoint logic). Can partially run in parallel with Phase 3 UI development.
- **UI/UX Implementation (Phase 5)**: Can start in parallel with Phases 3 and 4 once basic API/chat endpoints are available for integration. Requires stable frontend setup.
- **Testing & Validation (Phase 6)**: Depends on completion of all implementation phases.
- **Polish & Cross-Cutting Concerns (Phase 7)**: Depends on completion of all implementation and testing phases.

### Within Each Phase

- Tasks marked [P] can run in parallel.
- Entity/Model creation before services that use them.
- Services before API endpoints that expose them.
- Tests (if included) MUST be written and FAIL before implementation.

### Parallel Opportunities

- Most tasks within Phase 1 (Setup).
- Tasks T011 and T012 within Phase 2 (Foundational).
- Tasks T022 and T023 within Phase 4 (Conversational Interface).
- Many tasks within Phase 5 (UI/UX) once basic layout is established.
- Tasks T031, T032, T033, T034 within Phase 6 (Testing).

---

## Implementation Strategy

### MVP First (Phases 1, 2, 3, 4 with minimal UI, and initial Test/Validate)

1.  Complete Phase 1: Setup.
2.  Complete Phase 2: Foundational (CRITICAL - blocks most other work).
3.  Complete Phase 3: MCP Server & AI Agent Core.
4.  Complete Phase 4: Conversational Interface (initial chat endpoint + basic UI integration).
5.  Perform initial tests and validation from Phase 6 relevant to these components.
6.  **STOP and VALIDATE**: Test core chat functionality (AI agent interpreting and responding).
7.  Deploy/demo if ready for feedback.

### Incremental Delivery

1.  Complete Setup + Foundational → Core backend services ready.
2.  Add MCP Server & AI Agent Core → AI agent can process commands via MCP.
3.  Add Conversational Interface → Basic chat functionality live.
4.  Add UI/UX Implementation → Refined, professional UI.
5.  Each increment adds testable and demonstrable value.

---

## Notes

- [P] tasks = different files, no dependencies within the immediate context.
- [AC-XXX] label maps task to specific Acceptance Criteria for traceability.
- Each major phase should ideally be independently completable and testable.
- Verify tests fail before implementing.
- Commit after each task or logical group.
- Stop at any checkpoint to validate independently.
- Avoid: vague tasks, same file conflicts, cross-phase dependencies that break independence.
