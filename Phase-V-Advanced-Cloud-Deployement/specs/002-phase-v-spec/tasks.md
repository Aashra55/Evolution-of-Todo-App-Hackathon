# Tasks for Todo AI Chatbot Phase V - Advanced Cloud Deployment

**Feature Branch**: `002-phase-v-spec`
**Date**: 2026-02-09
**Plan**: [specs/002-phase-v-spec/plan.md](specs/002-phase-v-spec/plan.md)
**Spec**: [specs/002-phase-v-spec/spec.md](specs/002-phase-v-spec/spec.md)

## Summary

This document outlines the actionable, dependency-ordered tasks for Phase V of the Todo AI Chatbot, focusing on its transformation into an event-driven, agentic microservices system deployed on Kubernetes using Dapr and Kafka-style messaging, adhering to free-first infrastructure.

## Task Generation Methodology

Tasks are generated from design artifacts (`plan.md`, `spec.md`, `data-model.md`, `research.md`, API contracts) and organized by user story priority. Each task includes an ID, priority marker `[P]` if parallelizable, user story label `[USx]` where applicable, a clear description with exact file paths, and follows the strict checklist format.

## Dependency Graph (User Story Completion Order)

1.  **Phase 3: User Story 1** (Basic Task Management) - (P1)
2.  **Phase 4: User Story 2** (Advanced Task Attributes) - (P1)
3.  **Phase 5: User Story 4** (Agentic Workflow & CI/CD) - (P1)
4.  **Phase 6: User Story 3** (Real-time Multi-client Awareness) - (P2)

*Note: Phase 1 (Setup) and Phase 2 (Foundational) MUST be completed before Phase 3.*

## Parallel Execution Opportunities

-   **Frontend vs. Backend Services**: Initial scaffolding and basic UI/API for US1 can be developed in parallel.
-   **Individual Microservices**: Development of Notification, Recurring Task, Audit Log, and Real-time Sync services can be parallelized post-foundational infrastructure setup.
-   **Testing**: Unit, component, and E2E tests can be developed concurrently with their corresponding implementation tasks.

## Suggested MVP Scope

The Minimum Viable Product (MVP) for Phase V focuses on **User Story 1: Create/Manage Basic Todo Tasks**. This ensures core CRUD functionality is operational within the new microservices architecture, forming a stable base for subsequent development.

## Tasks

### Phase 1: Setup

Goal: Initialize project structure, dependencies, and basic configuration.

-   [ ] T001 Create base project directories: `frontend/`, `services/`, `services/chat-api/`, `services/notification/`, `services/recurring-task/`, `services/audit-log/`, `services/real-time-sync/`
-   [ ] T002 Configure base `frontend/` Next.js project: `frontend/package.json`, `frontend/next.config.js`
-   [ ] T003 Configure base `services/chat-api/` FastAPI project: `services/chat-api/requirements.txt`, `services/chat-api/main.py`
-   [ ] T004 Configure base `services/notification/` FastAPI project: `services/notification/requirements.txt`, `services/notification/main.py`
-   [ ] T005 Configure base `services/recurring-task/` FastAPI project: `services/recurring-task/requirements.txt`, `services/recurring-task/main.py`
-   [ ] T006 Configure base `services/audit-log/` FastAPI project: `services/audit-log/requirements.txt`, `services/audit-log/main.py`
-   [ ] T007 Configure base `services/real-time-sync/` FastAPI project: `services/real-time-sync/requirements.txt`, `services/real-time-sync/main.py`
-   [ ] T008 Create base `k8s/` directory structure for manifests.
-   [ ] T009 Create Dapr component manifests for Minikube (Pub/Sub: `task-events`, `reminders`, `task-updates`): `k8s/dapr/pubsub.yaml`
-   [ ] T010 Create Dapr component manifests for Minikube (State Store: `conversationstate`): `k8s/dapr/state.yaml`
-   [ ] T011 Configure basic Dockerfiles for each service: `frontend/Dockerfile`, `services/chat-api/Dockerfile`, `services/notification/Dockerfile`, `services/recurring-task/Dockerfile`, `services/audit-log/Dockerfile`, `services/real-time-sync/Dockerfile`

### Phase 2: Foundational (Core Infrastructure & Base Services)

Goal: Establish core communication, data persistence, and foundational services for event-driven architecture.

-   [ ] T012 Implement Task and User models for PostgreSQL: `services/chat-api/src/models/task.py`, `services/chat-api/src/models/user.py`
-   [ ] T013 Integrate Dapr Pub/Sub component into Chat API service for event publishing: `services/chat-api/src/main.py`
-   [ ] T014 Publish `TaskCreated` event via Dapr Pub/Sub upon new task creation: `services/chat-api/src/services/task_service.py`
-   [ ] T015 Publish `TaskUpdated` event via Dapr Pub/Sub upon task modification: `services/chat-api/src/services/task_service.py`
-   [ ] T016 Publish `TaskDeleted` event via Dapr Pub/Sub upon task deletion: `services/chat-api/src/services/task_service.py`
-   [ ] T017 Implement basic Dapr State Management for Conversation State in Chat API: `services/chat-api/src/services/conversation_state_service.py`
-   [ ] T018 Configure Dapr components for Minikube (PostgreSQL state store for tasks/users if in-cluster; or external Neon DB connection): `k8s/dapr/state-postgresql.yaml`
-   [ ] T019 Set up local Kafka-style messaging (Strimzi Kafka Operator) in Minikube: `k8s/kafka/strimzi-operator.yaml`, `k8s/kafka/kafka-cluster.yaml`, `k8s/kafka/topics.yaml`
-   [ ] T020 Deploy all services to Minikube with Dapr sidecars and verify basic connectivity: `k8s/minikube-deploy.sh`

### Phase 3: User Story 1 - Create/Manage Basic Todo Tasks (P1)

Goal: Enable users to perform fundamental CRUD operations on todo tasks via the chat interface, consistent with prior phases, within the microservices architecture.

**Independent Test Criteria**: A user can send a chat message to create a task, view it, update its title/description, mark it complete, and delete it. All operations are reflected correctly and persistently.

-   [ ] T021 [P] [US1] Implement FastAPI endpoint for GET /tasks in `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T022 [P] [US1] Implement FastAPI endpoint for POST /tasks in `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T023 [P] [US1] Implement FastAPI endpoint for GET /tasks/{task_id} in `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T024 [P] [US1] Implement FastAPI endpoint for PUT /tasks/{task_id} in `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T025 [P] [US1] Implement FastAPI endpoint for DELETE /tasks/{task_id} in `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T026 [P] [US1] Implement FastAPI endpoint for POST /tasks/{task_id}/complete in `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T027 [P] [US1] Implement chat interface in Frontend for task creation: `frontend/src/pages/chat.js`
-   [ ] T028 [P] [US1] Implement chat interface in Frontend for task listing and detail view: `frontend/src/pages/chat.js`
-   [ ] T029 [P] [US1] Implement chat interface in Frontend for task updates (e.g., mark complete, edit): `frontend/src/pages/chat.js`
-   [ ] T030 [P] [US1] Implement chat interface in Frontend for task deletion: `frontend/src/pages/chat.js`
-   [ ] T031 [US1] Integrate Chat API with Frontend for task CRUD operations: `frontend/src/services/chat_api.js`
-   [ ] T032 [US1] Unit tests for Chat API task CRUD operations: `services/chat-api/tests/unit/test_task_crud.py`
-   [ ] T033 [US1] Component tests for Frontend task components: `frontend/tests/components/task_list.test.js`
-   [ ] T034 [US1] E2E test for basic task CRUD via chat interface: `e2e/task_crud.spec.js`

### Phase 4: User Story 2 - Manage Advanced Task Attributes (P1)

Goal: Allow users to assign priorities, tags, due dates, reminders, recurring patterns, and use search/filter/sort for tasks.

**Independent Test Criteria**: A user can set/modify all advanced attributes for a task, search/filter/sort tasks based on these attributes, and recurring tasks are generated, with reminders scheduled and sent.

-   [ ] T035 [P] [US2] Extend Task model with `priority`, `tags`, `dueDate`, `reminderSettings`, `recurrencePattern`: `services/chat-api/src/models/task.py`
-   [ ] T036 [P] [US2] Update Chat API endpoints for `POST /tasks` and `PUT /tasks/{task_id}` to handle new attributes: `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T037 [P] [US2] Implement search, filter, and sort logic in Chat API: `services/chat-api/src/services/task_query_service.py`
-   [ ] T038 [P] [US2] Implement FastAPI endpoint for GET /tasks with query parameters for search/filter/sort: `services/chat-api/src/api/endpoints/tasks.py`
-   [ ] T039 [P] [US2] Implement FastAPI endpoint for POST /reminders to schedule reminders: `services/chat-api/src/api/endpoints/reminders.py`
-   [ ] T040 [P] [US2] Implement FastAPI endpoint for POST /recurring-tasks to define recurring tasks: `services/chat-api/src/api/endpoints/recurring_tasks.py`
-   [ ] T041 [P] [US2] Implement Notification Service to consume `reminders` topic via Dapr Pub/Sub: `services/notification/src/main.py`
-   [ ] T042 [P] [US2] Implement logic in Notification Service to send notifications: `services/notification/src/services/notification_sender.py`
-   [ ] T043 [P] [US2] Implement Recurring Task Service to consume `task-events` and use Dapr Scheduled Jobs for recurrence logic: `services/recurring-task/src/main.py`
-   [ ] T044 [P] [US2] Implement logic in Recurring Task Service to generate new tasks based on patterns: `services/recurring-task/src/services/recurrence_generator.py`
-   [ ] T045 [US2] Update Frontend chat interface to allow setting advanced attributes for tasks: `frontend/src/pages/chat.js`
-   [ ] T046 [US2] Update Frontend task list to display advanced attributes and enable search/filter/sort in UI: `frontend/src/pages/chat.js`
-   [ ] T047 [US2] Unit tests for advanced task attribute handling in Chat API: `services/chat-api/tests/unit/test_advanced_task.py`
-   [ ] T048 [US2] Unit tests for Notification Service logic: `services/notification/tests/unit/test_notification_service.py`
-   [ ] T049 [US2] Unit tests for Recurring Task Service logic: `services/recurring-task/tests/unit/test_recurrence_logic.py`
-   [ ] T050 [US2] E2E test for setting advanced task attributes and verifying behavior: `e2e/advanced_task_attributes.spec.js`
-   [ ] T051 [US2] E2E test for search/filter/sort functionality: `e2e/task_query.spec.js`
-   [ ] T052 [US2] E2E test for recurring task generation and reminder scheduling: `e2e/recurring_reminders.spec.js`

### Phase 5: User Story 4 - Agentic Workflow Compliance (P1)

Goal: Establish a CI/CD pipeline and secrets management strategy that complies with the agentic workflow and free-first principles.

**Independent Test Criteria**: A pull request triggers a GitHub Actions workflow that builds, tests, and deploys the application (to Minikube or staging OKE), and secrets are securely managed without hardcoding.

-   [ ] T053 [P] [US4] Set up GitHub Actions workflow for CI (lint, unit tests, build container images): `.github/workflows/ci.yaml`
-   [ ] T054 [P] [US4] Set up GitHub Actions workflow for CD (deploy to Minikube): `.github/workflows/cd-minikube.yaml`
-   [ ] T055 [P] [US4] Configure Kubernetes Secrets for sensitive data: `k8s/secrets/app-secrets.yaml`
-   [ ] T056 [P] [US4] Integrate Dapr Secrets management component in services to access Kubernetes Secrets: `k8s/dapr/secretstore.yaml`, `services/*/src/config/secrets.py` (or similar)
-   [ ] T057 [US4] E2E test: Verify CI/CD pipeline successfully builds and deploys to Minikube: `e2e/ci_cd_workflow.spec.js`
-   [ ] T058 [US4] Manual verification: Ensure no hardcoded secrets or connection strings exist in codebase.

### Phase 6: User Story 3 - Real-time Multi-client Awareness (P2)

Goal: Implement real-time synchronization of task changes across multiple connected clients.

**Independent Test Criteria**: Modifying a task from one client results in immediate and accurate reflection of the change on another connected client.

-   [ ] T059 [P] [US3] Implement WebSocket server in Real-time Sync Service: `services/real-time-sync/src/main.py`
-   [ ] T060 [P] [US3] Implement logic in Real-time Sync Service to consume `task-events` and `task-updates` via Dapr Pub/Sub: `services/real-time-sync/src/main.py`
-   [ ] T061 [P] [US3] Implement logic to translate Dapr events into client-specific WebSocket messages: `services/real-time-sync/src/services/message_formatter.py`
-   [ ] T062 [P] [US3] Implement logic to broadcast WebSocket messages to connected clients: `services/real-time-sync/src/services/websocket_manager.py`
-   [ ] T063 [US3] Implement WebSocket client in Frontend to connect to Real-time Sync Service: `frontend/src/services/realtime_sync.js`
-   [ ] T064 [US3] Update Frontend UI components to react to real-time task updates: `frontend/src/components/task_list.js`, `frontend/src/pages/chat.js`
-   [ ] T065 [US3] E2E test for real-time synchronization across two client instances: `e2e/realtime_sync.spec.js`

### Final Phase: Polish & Cross-Cutting Concerns

Goal: Ensure the system is robust, observable, and ready for cloud deployment.

-   [ ] T066 [P] Implement structured logging for all services: `services/*/src/config/logging.py`, `services/*/src/main.py`
-   [ ] T067 [P] Implement minimal metrics exposure for all services (e.g., Prometheus compatible): `services/*/src/main.py`
-   [ ] T068 [P] Implement correlation ID propagation across services via Dapr context: `services/*/src/middleware/correlation.py`
-   [ ] T069 [P] Configure Dapr mTLS for all inter-service communication: `k8s/dapr/config.yaml`
-   [ ] T070 [P] Implement robust error handling and retry mechanisms using Dapr resilience policies: `k8s/dapr/resilience.yaml`
-   [ ] T071 [P] Configure Oracle Cloud OKE deployment with Helm charts for all services: `helm/todo-app/Chart.yaml`, `helm/todo-app/values.yaml`, `helm/todo-app/templates/*.yaml`
-   [ ] T072 [P] Integrate CI/CD pipeline (GitHub Actions) for deployment to Oracle Cloud OKE: `.github/workflows/cd-oke.yaml`
-   [ ] T073 [P] Create comprehensive README.md files for each service and the monorepo root.
-   [ ] T074 Final E2E testing of the full system on OKE.
-   [ ] T075 Performance testing for key user flows.
-   [ ] T076 Security audit and penetration testing (conceptual).