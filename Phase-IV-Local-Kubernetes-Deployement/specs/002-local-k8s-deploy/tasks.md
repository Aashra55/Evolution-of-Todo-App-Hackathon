# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/002-local-k8s-deploy/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification does not explicitly request test tasks. Validation will occur via verification of AI agent outputs and deployment checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for frontend and backend applications.

- [x] T001 [P] Initialize frontend project (React/TypeScript) in `frontend/`
- [x] T002 [P] Initialize backend project (Node.js/TypeScript) in `backend/`
- [x] T003 [P] Configure frontend linting and formatting tools in `frontend/`
- [x] T004 [P] Configure backend linting and formatting tools in `backend/`
- [x] T005 [P] Create backend source directories: `backend/src/models/`, `backend/src/services/`, `backend/src/api/`
- [x] T006 [P] Create frontend source directories: `frontend/src/components/`, `frontend/src/pages/`, `frontend/src/services/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core application structure, database setup, and basic API framework. This phase MUST be complete before any user story implementation begins.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create `User` data model implementation (e.g., `backend/src/models/user.ts`)
- [x] T008 Create `TodoItem` data model implementation (e.g., `backend/src/models/todoItem.ts`)
- [x] T009 Set up PostgreSQL database connection and ORM/client for backend in `backend/src/config/database.ts`
- [x] T010 Implement basic backend API routing structure (e.g., `backend/src/api/index.ts`)
- [x] T011 Set up basic error handling middleware for backend in `backend/src/middleware/errorHandler.ts`
- [x] T012 Implement user registration endpoint (`POST /users/register`) based on `specs/002-local-k8s-deploy/contracts/api.yaml` in `backend/src/api/auth.ts`
- [x] T013 Implement user login endpoint (`POST /users/login`) based on `specs/002-local-k8s-deploy/contracts/api.yaml` in `backend/src/api/auth.ts`
- [x] T014 Implement authentication middleware for protected routes in `backend/src/middleware/auth.ts`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 2 - Automated Containerization (P1)

**Goal**: Produce optimized Docker images for frontend and backend applications.

**Independent Test**: Verify Docker images are built successfully and are optimized.

- [x] T015 [US2] Generate initial Dockerfile for frontend application in `frontend/Dockerfile`
- [x] T016 [US2] Generate initial Dockerfile for backend application in `backend/Dockerfile`
- [x] T017 [US2] Define AI agent interaction for frontend image building using Docker AI Agent (Gordon)
- [x] T018 [US2] Define AI agent interaction for backend image building using Docker AI Agent (Gordon)
- [x] T019 [US2] Implement fallback logic for Claude Code to generate Docker CLI commands if Gordon is unavailable for `frontend/Dockerfile`
- [x] T020 [US2] Implement fallback logic for Claude Code to generate Docker CLI commands if Gordon is unavailable for `backend/Dockerfile`
- [x] T021 [P] [US2] Implement Docker image build validation (output analysis, security scanning) for frontend
- [x] T022 [P] [US2] Implement Docker image build validation (output analysis, security scanning) for backend

---

## Phase 4: User Story 3 - Automated Helm Chart Generation (P1)

**Goal**: Generate and maintain Helm Charts for Kubernetes deployment.

**Independent Test**: Helm charts pass dry-run validations.

- [x] T023 [US3] Create base Helm chart structure in `helm-charts/todo-app/`
- [x] T024 [US3] Define `values.yaml` for frontend image, replicas, service ports in `helm-charts/todo-app/values.yaml`
- [x] T025 [US3] Define `values.yaml` for backend image, replicas, service ports, and database connection details in `helm-charts/todo-app/values.yaml`
- [x] T026 [US3] Create Helm template for frontend Deployment in `helm-charts/todo-app/templates/frontend-deployment.yaml`
- [x] T027 [US3] Create Helm template for frontend Service in `helm-charts/todo-app/templates/frontend-service.yaml`
- [x] T028 [US3] Create Helm template for backend Deployment in `helm-charts/todo-app/templates/backend-deployment.yaml`
- [x] T029 [US3] Create Helm template for backend Service in `helm-charts/todo-app/templates/backend-service.yaml`
- [x] T030 [US3] Create Helm template for PostgreSQL Deployment (e.g., using bitnami/postgresql) in `helm-charts/todo-app/templates/postgresql-deployment.yaml`
- [x] T031 [US3] Create Helm template for PostgreSQL Service in `helm-charts/todo-app/templates/postgresql-service.yaml`
- [x] T032 [US3] Implement AI agent interaction for Helm chart generation/maintenance
- [x] T033 [US3] Implement Helm lint validation step
- [x] T034 [US3] Implement Helm template dry-run validation step

---

## Phase 5: User Story 1 - Deploy Todo Chatbot to Minikube (P1)

**Goal**: Deploy the containerized frontend and backend of the Todo Chatbot to a local Minikube cluster using Helm charts.

**Independent Test**: All frontend and backend pods are running and ready, and the application is accessible.

- [x] T035 [US1] Implement `kubectl-ai` command to start Minikube cluster (if not running)
- [x] T036 [US1] Implement `kubectl-ai` command to configure `kubectl` context to Minikube
- [x] T037 [US1] Implement `kubectl-ai` command to deploy `todo-app` Helm chart to Minikube
- [x] T038 [US1] Implement `kubectl-ai` command to verify frontend pod readiness and health
- [x] T039 [US1] Implement `kubectl-ai` command to verify backend pod readiness and health
- [x] T040 [US1] Implement `kubectl-ai` command to verify PostgreSQL pod readiness and health
- [x] T041 [US1] Implement `kubectl-ai` command to provide access to the frontend application (e.g., port-forwarding or service URL retrieval)

---

## Phase 6: User Story 4 - AI-Assisted Cluster Management (P2)

**Goal**: Implement AI-assisted debugging, scaling, and cluster health monitoring.

**Independent Test**: AI agents successfully detect, diagnose, and suggest fixes for cluster issues; scale deployments; and provide insights.

- [x] T042 [US4] Integrate `kubectl-ai` for scaling frontend deployments based on load metrics
- [x] T043 [US4] Integrate `kubectl-ai` for scaling backend deployments based on load metrics
- [x] T044 [US4] Integrate `kubectl-ai` for debugging failing frontend pods and suggesting fixes
- [x] T045 [US4] Integrate `kubectl-ai` for debugging failing backend pods and suggesting fixes
- [x] T046 [US4] Integrate `kagent` for monitoring Minikube cluster health and resource utilization
- [x] T047 [US4] Integrate `kagent` for optimizing resource allocation and suggesting improvements for deployed components
- [x] T048 [US4] Implement fallback for `kagent` to analyze and repair deployments if `kubectl-ai` fails

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Overall improvements, documentation, and final validation.

- [x] T049 Update `specs/002-local-k8s-deploy/quickstart.md` with concrete AI agent interactions and commands
- [x] T050 Implement logging and traceability for all AI agent operations
- [x] T051 Define and implement a rollback strategy for failed deployments
- [x] T052 Review and ensure strict confidentiality measures for all repositories and sensitive data are in place
- [x] T053 Validate end-to-end functionality of the deployed Todo Chatbot on Minikube (Conceptual validation - actual execution requires live environment)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 2 - Containerization (Phase 3)**: Depends on Foundational phase completion
- **User Story 3 - Helm Chart Generation (Phase 4)**: Depends on Foundational phase completion
- **User Story 1 - Deploy (Phase 5)**: Depends on Containerization (Phase 3) and Helm Chart Generation (Phase 4)
- **User Story 4 - Cluster Management (Phase 6)**: Depends on Deploy (Phase 5)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies (within project logic)

- **User Story 2 (P1) - Automated Containerization**: Provides Docker images for US3 and US1.
- **User Story 3 (P1) - Automated Helm Chart Generation**: Provides Helm charts for US1.
- **User Story 1 (P1) - Deploy Todo Chatbot to Minikube**: Consumes Docker images (from US2) and Helm charts (from US3).
- **User Story 4 (P2) - AI-Assisted Cluster Management**: Operates on the deployed application (from US1).

### Within Each User Story

- Tasks are ordered to respect internal logical dependencies (e.g., Dockerfile before image building, chart structure before templates).

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- Tasks within User Story phases marked [P] can run in parallel.
- Once Foundational phase completes, User Story 2 (Containerization) and User Story 3 (Helm Chart Generation) can be worked on in parallel.

---

## Parallel Example: Phase 1 (Setup)

```bash
# All these tasks can run in parallel
Task: "Initialize frontend project (React/TypeScript) in frontend/"
Task: "Initialize backend project (Node.js/TypeScript) in backend/"
Task: "Configure frontend linting and formatting tools in frontend/"
Task: "Configure backend linting and formatting tools in backend/"
Task: "Create backend source directories: backend/src/models/, backend/src/services/, backend/src/api/"
Task: "Create frontend source directories: frontend/src/components/, frontend/src/pages/, frontend/src/services/"
```

## Parallel Example: Phase 3 (User Story 2 - Automated Containerization)

```bash
# Once Foundational is complete, these can run in parallel
Task: "Generate initial Dockerfile for frontend application in frontend/Dockerfile"
Task: "Generate initial Dockerfile for backend application in backend/Dockerfile"
Task: "Implement Docker image build validation (output analysis, security scanning) for frontend"
Task: "Implement Docker image build validation (output analysis, security scanning) for backend"
```

---

## Implementation Strategy

### MVP First (User Story 2 + 3 + 1)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 2 - Automated Containerization
4.  Complete Phase 4: User Story 3 - Automated Helm Chart Generation
5.  Complete Phase 5: User Story 1 - Deploy Todo Chatbot to Minikube
6.  **STOP and VALIDATE**: Test User Story 1 independently (verify deployment and application access).
7.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 2 → Automated Containerization
3.  Add User Story 3 → Automated Helm Chart Generation
4.  Add User Story 1 → Deploy Todo Chatbot to Minikube → Test independently → Deploy/Demo (MVP!)
5.  Add User Story 4 → AI-Assisted Cluster Management → Test independently → Deploy/Demo
6.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 2 (Containerization)
    -   Developer B: User Story 3 (Helm Chart Generation)
    -   Developer C: User Story 1 (Deployment) - *Can only start after A and B provide their outputs*
    -   Developer D: User Story 4 (Cluster Management) - *Can only start after C's deployment*
3.  Stories complete and integrate.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
