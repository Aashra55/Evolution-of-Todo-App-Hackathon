# Tasks: Multi-User Web Application

**Input**: Design documents from `/specs/003-full-stack-webapp/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api.yaml

## Path Conventions

- **Backend**: `src/backend/`
- **Frontend**: `src/frontend/`

---

## Phase 1: Project Setup

**Purpose**: Initialize the backend and frontend project structures.

- [ ] T001 Initialize a new Python project using Poetry in `src/backend/`.
- [ ] T002 Add FastAPI, SQLModel, Alembic, uvicorn, python-jose, and passlib as dependencies in `src/backend/pyproject.toml`.
- [ ] T003 [P] Initialize a new Next.js project (App Router) in `src/frontend/`.
- [ ] T004 [P] Create an initial `.env.example` file in `src/backend/` with `DATABASE_URL` and `SECRET_KEY` placeholders.
- [ ] T005 [P] Create an initial `.env.local.example` file in `src/frontend/` with a `NEXT_PUBLIC_API_BASE_URL` placeholder.

---

## Phase 2: Foundational (Backend Database)

**Purpose**: Establish the core database configuration, models, and migration framework. This phase blocks all other development.

- [ ] T006 Create a database connection module in `src/backend/database.py`.
- [ ] T007 Implement the User and Task models in `src/backend/models.py` based on `data-model.md`.
- [ ] T008 Configure Alembic for database migrations in `src/backend/`.
- [ ] T009 Generate an initial Alembic migration script for the User and Task tables.

**Checkpoint**: Foundation ready. User story implementation can begin.

---

## Phase 3: User Story 1 - Secure Authentication & Data Isolation

**Goal**: Allow users to sign up, log in, and ensure they can only access their own data. This combines US1 and the core principle of US3 from the spec.

**Independent Test**: A new user can create an account and log in. A second user can also create an account and log in. Neither user can see or affect the data of the other.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create Pydantic schemas for User/Token data transfer in `src/backend/schemas.py`.
- [ ] T011 [P] [US1] Implement JWT creation and password hashing logic in `src/backend/security.py`.
- [ ] T012 [P] [US1] Create a dependency to get the current authenticated user from a JWT in `src/backend/dependencies.py`.
- [ ] T013 [US1] Implement the `/auth/signup` and `/auth/token` API endpoints in `src/backend/routers/auth.py`.
- [ ] T014 [P] [US1] Create the UI components for Sign Up and Sign In pages in `src/frontend/app/(auth)/`.
- [ ] T015 [P] [US1] Create an API client service in `src/frontend/services/api.js` to communicate with the backend.
- [ ] T016 [US1] Implement the frontend logic for user registration, login, JWT storage, and logout.

**Checkpoint**: User authentication is functional. Users can log in and receive a token.

---

## Phase 4: User Story 2 - Task Management

**Goal**: Enable logged-in users to create, view, update, and delete their own tasks.

**Independent Test**: A logged-in user can add a task, see it in their list, edit it, mark it complete, and delete it. The changes are persisted and visible upon refresh.

### Implementation for User Story 2

- [ ] T017 [P] [US2] Add Pydantic schemas for Task data transfer to `src/backend/schemas.py`.
- [ ] T018 [US2] Implement the CRUD API endpoints for tasks in `src/backend/routers/tasks.py`. Ensure all database operations are scoped to the authenticated user provided by the dependency from T012.
- [ ] T019 [P] [US2] Create the main task dashboard UI component in `src/frontend/app/dashboard/page.jsx`.
- [ ] T020 [P] [US2] Create reusable UI components for the task list, a single task item, and a task creation form in `src/frontend/components/tasks/`.
- [ ] T021 [US2] Implement frontend logic in the dashboard to fetch, create, update, and delete tasks using the API client service.

**Checkpoint**: Full CRUD functionality for tasks is complete and integrated.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Finalize the application with error handling, documentation, and configuration.

- [ ] T022 [P] Implement global exception handling middleware in `src/backend/main.py`.
- [ ] T023 [P] Configure CORS middleware in `src/backend/main.py` to allow requests from the frontend.
- [ ] T024 [P] Write a comprehensive `README.md` for both the `src/backend` and `src/frontend` directories, explaining setup and execution.
- [ ] T025 [P] Add basic unit tests for the backend authentication logic in `src/backend/tests/`.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed before all other phases.
- **Phase 2 (Foundational)** depends on Phase 1. It blocks all user story phases.
- **Phase 3 (US1)** depends on Phase 2.
- **Phase 4 (US2)** depends on Phase 3, as it requires the user authentication and data scoping mechanisms.
- **Phase 5 (Polish)** can be worked on incrementally but should be finalized after all features are complete.

## Implementation Strategy

The project will follow an MVP-first, incremental delivery model.

1.  **Foundation (Phase 1 & 2)**: Complete the project setup and database foundation first.
2.  **MVP (Phase 3)**: Implement User Story 1 (Authentication). At this point, the core security model is testable.
3.  **Feature Complete (Phase 4)**: Implement User Story 2 (Task Management). The application is now fully functional.
4.  **Finalize (Phase 5)**: Add polish and final documentation.
