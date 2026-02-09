# Feature Specification: Todo AI Chatbot Phase V - Advanced Cloud Deployment

**Feature Branch**: `002-phase-v-spec`  
**Created**: 2026-02-09  
**Status**: Draft  
**Input**: User description: "Generate specs considering the following details: You are Spec-Kit Plus operating in SPECIFICATION mode. Your task is to generate a COMPLETE, EXHAUSTIVE, and JUDGE-READY TECHNICAL SPECIFICATION for Phase V of the project described below. You MUST strictly comply with the already-defined Project Constitution. Assume that judges will disqualify any output that violates the constitution. ==================================================== CRITICAL OUTPUT RULES ==================================================== - Produce a SINGLE cohesive specification document - NO architecture diagrams (text, Mermaid, ASCII, or images) - Architecture must be described using structured text only - NO explanations, NO commentary, NO teaching tone - Use enforceable language (MUST / SHALL / MUST NOT) ==================================================== PROJECT CONTEXT ==================================================== Project Name: Todo AI Chatbot Phase: Phase V – Advanced Cloud Deployment Project Intent: Transform the Todo AI Chatbot from a CRUD-based app into a production-style, event-driven, agentic microservices system using Kubernetes, Kafka-style messaging, and Dapr. Primary Evaluation Criteria: - Event-driven correctness - Use of Dapr as abstraction (not decoration) - Free-infrastructure discipline - Spec-driven, agentic development maturity ==================================================== INFRASTRUCTURE CONSTRAINTS (STRICT) ==================================================== - ALL infrastructure MUST be free or always-free - NO paid services - NO mandatory use of expiring trial credits - Local environment: Minikube - Cloud environment: Oracle Cloud OKE (always-free) - Kafka: Self-hosted within Kubernetes OR free serverless tier - CI/CD: GitHub Actions (free tier) Any service violating these constraints MUST be excluded. ==================================================== DEVELOPMENT METHODOLOGY (MANDATORY) ==================================================== The entire project MUST follow the Agentic Dev Stack: 1. Specification-first development 2. Execution plan generated from spec 3. Task breakdown derived from plan 4. Implementation via Claude Code ONLY 5. NO manual coding or ad-hoc edits 6. All changes validated against constitution and specs The spec MUST define rules that enforce this workflow. ==================================================== FUNCTIONAL SCOPE (MANDATORY) ==================================================== The specification MUST include ALL prior-level functionality: Basic Level: - Core task CRUD via chat interface Intermediate Level: - Task priorities - Tags - Search - Filter - Sorting Advanced Level: - Recurring tasks - Due dates - Reminders - Asynchronous task processing - Real-time multi-client awareness ==================================================== EVENT-DRIVEN SYSTEM REQUIREMENTS ==================================================== The Todo application MUST be re-architected around events. Kafka Topics (MANDATORY): - task-events - reminders - task-updates Required event use cases: 1. Reminder and notification scheduling 2. Recurring task generation 3. Activity / audit log 4. Real-time client synchronization For EACH event type, define: - Triggering condition - Event producer - Event consumers - Guaranteed delivery expectations - Ordering assumptions - Idempotency behavior - Failure and retry semantics (conceptual) ==================================================== SERVICE ARCHITECTURE SPECIFICATION ==================================================== Define each service in isolation and in interaction: Services to specify: - Frontend Service (Next.js) - Chat API Service (FastAPI + MCP tools) - Notification Service - Recurring Task Service - Audit / Activity Log Service - Real-time Sync Service For EACH service define: - Core responsibilities - Public interfaces (conceptual) - Events published - Events consumed - Dapr APIs used - Stateless vs stateful classification - Horizontal scalability expectations ==================================================== DAPR USAGE (NON-NEGOTIABLE) ==================================================== Dapr MUST be the ONLY integration layer for: - Pub/Sub (Kafka abstraction) - State Management - Service Invocation - Scheduled jobs (Jobs API or Bindings) - Secrets management The specification MUST explicitly forbid: - Direct Kafka client usage in application code - Direct DB drivers where Dapr state store is defined - Hardcoded connection strings ==================================================== STATE & DATA MANAGEMENT ==================================================== Define: - What data is stored in PostgreSQL (Neon or in-cluster) - What data is stored via Dapr State Store - Conversation state handling - Task state vs event history separation - Data retention and cleanup policies No SQL schemas required, only conceptual structure. ==================================================== DEPLOYMENT SPECIFICATION ==================================================== Local Deployment (Minikube): - Namespaces - Component installation order - Kafka setup approach - Validation checklist (what proves it works) Cloud Deployment (Oracle Cloud OKE): - Environment parity with local - Helm-based deployment assumptions - Config separation (dev vs cloud) - Cost-control principles ==================================================== CI/CD PIPELINE (FREE-TIER SAFE) ==================================================== Using GitHub Actions, specify: - Trigger conditions - Build stages - Containerization strategy - Kubernetes deployment approach - Rollback philosophy ==================================================== SECURITY & RESILIENCE ==================================================== Specify: - Secret handling (Kubernetes + Dapr) - mTLS via Dapr - Failure scenarios (Kafka down, service crash) - Backoff and retry approach - Graceful degradation ==================================================== OBSERVABILITY ==================================================== Define: - Logging expectations - Minimal metrics - Traceability via event IDs - Debugging strategy without paid tools ==================================================== DELIVERABLES ==================================================== The specification MUST clearly define: - Repository structure - /specs folder structure - Phase separation conventions - README requirements - Demo expectations (≤90 seconds) ==================================================== SUCCESS CRITERIA ==================================================== Define what it means for Phase V to be "COMPLETE": - Functional completeness - Architectural correctness - Agentic workflow compliance - Zero-cost infrastructure compliance ==================================================== OUTPUT FORMAT ==================================================== - ONE specification document - Clear sectioning - Enforceable language - No diagrams - No extra explanations Return ONLY the specification document.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create/Manage Basic Todo Tasks (Priority: P1)

A user MUST be able to create, read, update, and delete (CRUD) todo tasks via the chat interface, consistent with prior phase functionality.

**Why this priority**: This forms the fundamental core functionality of a Todo application and is essential for any user interaction.

**Independent Test**: Can be fully tested by creating a task, updating it, completing it, and deleting it through the chat interface and observing corresponding updates.

**Acceptance Scenarios**:

1. **Given** the user is in the chat interface, **When** the user sends a message to create a task, **Then** the task MUST be created and visible.
2. **Given** an existing task, **When** the user sends a message to update the task, **Then** the task MUST reflect the changes.
3. **Given** an existing task, **When** the user sends a message to delete the task, **Then** the task MUST be removed from the list.

### User Story 2 - Manage Advanced Task Attributes (Priority: P1)

A user MUST be able to assign priorities, tags, due dates, and reminders to tasks, search, filter, and sort tasks, and configure recurring tasks. The system MUST provide asynchronous processing for reminders and recurring task generation.

**Why this priority**: These features enhance task management capabilities significantly, directly contributing to user productivity and the "advanced" nature of Phase V.

**Independent Test**: Can be fully tested by applying various attributes to tasks, then using search/filter/sort, setting up recurring tasks, and verifying reminders are scheduled.

**Acceptance Scenarios**:

1. **Given** an existing task, **When** the user assigns a priority, **Then** the task's priority MUST be updated and reflected in listings.
2. **Given** an existing task, **When** the user assigns tags, **Then** the task MUST be associated with the tags and searchable by them.
3. **Given** a task with a due date and reminder, **When** the reminder trigger condition is met, **Then** the user MUST receive a notification.
4. **Given** a recurring task definition, **When** the recurrence condition is met, **Then** a new instance of the task MUST be generated.
5. **Given** a list of tasks, **When** the user applies search, filter, or sort criteria, **Then** the tasks MUST be displayed according to the criteria.

### User Story 3 - Real-time Multi-client Awareness (Priority: P2)

Multiple users interacting with the same task list (e.g., shared lists, or a single user across multiple devices) MUST experience real-time synchronization of task changes.

**Why this priority**: This feature supports collaborative use cases and provides a seamless experience across devices, leveraging the event-driven architecture.

**Independent Test**: Can be fully tested by modifying a task from one client/device and observing immediate updates on another connected client/device.

**Acceptance Scenarios**:

1. **Given** two clients connected to the system viewing the same task list, **When** a task is modified on Client A, **Then** Client B's view of the task list MUST update in real-time.
2. **Given** a task is created or deleted on Client A, **When** Client B is connected, **Then** Client B's view of the task list MUST update in real-time to reflect the change.

### User Story 4 - Agentic Workflow Compliance (Priority: P1)

The entire project development process, including this specification, MUST adhere to the Agentic Dev Stack methodology.

**Why this priority**: This is a primary evaluation criterion and defines the mandated development approach for the project.

**Independent Test**: Can be verified by auditing the project's artifact history (specs, plans, tasks, PHRs, ADRs) and confirming the absence of manual coding or ad-hoc edits.

**Acceptance Scenarios**:

1. **Given** any code change, **When** the change is reviewed, **Then** it MUST be traceable to a specific task derived from a plan, which in turn derived from a spec.
2. **Given** the project's development history, **When** an audit is performed, **Then** all changes MUST comply with the Agentic Dev Stack principles (spec-first, execution plan, task breakdown, Claude Code only).

### Edge Cases

- What happens when a reminder notification fails to send? The system MUST implement retry mechanisms with exponential backoff.
- How does the system handle concurrent updates to the same task from multiple clients? The system MUST employ optimistic concurrency control or last-write-wins based on business rules for specific fields.
- What if a Kafka-style messaging system is temporarily unavailable? Dapr MUST ensure guaranteed delivery of messages once the messaging system recovers.
- How does the system ensure data consistency across services in an event-driven architecture? Events MUST be designed to be idempotent where necessary to allow for safe retries.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Todo AI Chatbot MUST support creation, retrieval, updating, and deletion (CRUD) of todo tasks via a chat interface. (Basic Level)
- **FR-002**: The Todo AI Chatbot MUST allow users to assign priorities to tasks. (Intermediate Level)
- **FR-003**: The Todo AI Chatbot MUST allow users to assign tags to tasks. (Intermediate Level)
- **FR-004**: The Todo AI Chatbot MUST provide search functionality for tasks. (Intermediate Level)
- **FR-005**: The Todo AI Chatbot MUST provide filtering functionality for tasks based on various criteria (e.g., priority, tags, status). (Intermediate Level)
- **FR-006**: The Todo AI Chatbot MUST provide sorting functionality for tasks. (Intermediate Level)
- **FR-007**: The Todo AI Chatbot MUST support recurring tasks with configurable recurrence patterns. (Advanced Level)
- **FR-008**: The Todo AI Chatbot MUST allow users to set due dates for tasks. (Advanced Level)
- **FR-009**: The Todo AI Chatbot MUST allow users to set reminders for tasks. (Advanced Level)
- **FR-010**: The Todo AI Chatbot MUST implement asynchronous task processing for reminder scheduling and recurring task generation. (Advanced Level)
- **FR-011**: The Todo AI Chatbot MUST provide real-time multi-client awareness, synchronizing task changes across connected clients. (Advanced Level)

#### Event-Driven System Requirements

- **FR-012**: The Todo AI Chatbot MUST be re-architected around events.
- **FR-013**: The system MUST utilize `task-events` Kafka topic for general task lifecycle events (created, updated, completed, deleted).
- **FR-014**: The system MUST utilize `reminders` Kafka topic for reminder scheduling and notification events.
- **FR-015**: The system MUST utilize `task-updates` Kafka topic for real-time client synchronization.
- **FR-016**: **Reminder and Notification Scheduling**:
    - **Triggering condition**: Task due date approaching or user-defined reminder time.
    - **Event producer**: Notification Service / Scheduled Job (via Dapr).
    - **Event consumers**: Notification Service.
    - **Guaranteed delivery expectations**: MUST ensure at-least-once delivery.
    - **Ordering assumptions**: Order within a single task's reminders is preferred but not strictly required globally.
    - **Idempotency behavior**: Reminder processing MUST be idempotent to prevent duplicate notifications upon retry.
    - **Failure and retry semantics**: Conceptual - Automatic retry with exponential backoff for failed notification attempts.
- **FR-017**: **Recurring Task Generation**:
    - **Triggering condition**: Scheduled recurrence pattern for a task.
    - **Event producer**: Recurring Task Service / Scheduled Job (via Dapr).
    - **Event consumers**: Recurring Task Service, Chat API Service (for new task creation).
    - **Guaranteed delivery expectations**: MUST ensure at-least-once delivery.
    - **Ordering assumptions**: Not strictly required.
    - **Idempotency behavior**: New task creation from recurrence MUST be idempotent to prevent duplicate tasks.
    - **Failure and retry semantics**: Conceptual - Retry failed generation attempts; logic MUST prevent repeated task creation.
- **FR-018**: **Activity / Audit Log**:
    - **Triggering condition**: Any significant task lifecycle event (creation, update, deletion), or system-level action.
    - **Event producer**: Chat API Service, Recurring Task Service, Notification Service (any service performing an action).
    - **Event consumers**: Audit / Activity Log Service.
    - **Guaranteed delivery expectations**: MUST ensure at-least-once delivery.
    - **Ordering assumptions**: Causal ordering is preferred for events related to the same task.
    - **Idempotency behavior**: Audit log entries are typically additive; idempotency ensures consistent state capture on retries.
    - **Failure and retry semantics**: Conceptual - Retry failed log entries; log service MUST handle duplicate entries gracefully.
- **FR-019**: **Real-time Client Synchronization**:
    - **Triggering condition**: Any update to a task's state or attributes.
    - **Event producer**: Chat API Service, Recurring Task Service, Notification Service.
    - **Event consumers**: Real-time Sync Service.
    - **Guaranteed delivery expectations**: Best-effort delivery for timely updates, with eventual consistency for the full state.
    - **Ordering assumptions**: Order of updates for a single task MUST be preserved for client display accuracy.
    - **Idempotency behavior**: Client updates MUST be handled idempotently to prevent flicker or incorrect state on duplicate messages.
    - **Failure and retry semantics**: Conceptual - Focus on rapid re-delivery; clients capable of reconciling state.

#### Service Architecture Requirements

- **FR-020**: The system MUST consist of the following services: Frontend Service, Chat API Service, Notification Service, Recurring Task Service, Audit / Activity Log Service, Real-time Sync Service.
- **FR-021**: **Frontend Service (Next.js)**:
    - **Core responsibilities**: User interface, chat interaction, display of tasks and notifications.
    - **Public interfaces**: HTTP/WebSocket for interaction with Chat API and Real-time Sync Service.
    - **Events published**: None directly (interacts via API calls).
    - **Events consumed**: Task updates (via Real-time Sync Service).
    - **Dapr APIs used**: None directly (relies on backend services for Dapr interactions).
    - **Stateless vs stateful classification**: Stateless (session handled by backend).
    - **Horizontal scalability expectations**: High; MUST scale based on user load.
- **FR-022**: **Chat API Service (FastAPI + MCP tools)**:
    - **Core responsibilities**: Handle user chat commands, task CRUD operations, integrate with AI for natural language processing, orchestrate task events.
    - **Public interfaces**: HTTP REST API for Frontend, Dapr service invocation.
    - **Events published**: `task-events`, `task-updates`.
    - **Events consumed**: `task-events` (for internal state management/consistency if needed), `reminders` (for confirming scheduling), `task-updates` (for internal state consistency across service invocations).
    - **Dapr APIs used**: Pub/Sub, State Management (for conversation state), Service Invocation.
    - **Stateless vs stateful classification**: Stateless (task state in DB, conversation state via Dapr State Store).
    - **Horizontal scalability expectations**: High; MUST scale based on chat load.
- **FR-023**: **Notification Service**:
    - **Core responsibilities**: Schedule and send reminders (e.g., email, in-app), handle various notification channels.
    - **Public interfaces**: Dapr service invocation (e.g., for direct notification requests).
    - **Events published**: `reminders` (acknowledgements, status updates).
    - **Events consumed**: `reminders` (to process and send notifications).
    - **Dapr APIs used**: Pub/Sub, Scheduled Jobs (for triggering reminders), Bindings (for external notification systems).
    - **Stateless vs stateful classification**: Stateless.
    - **Horizontal scalability expectations**: Moderate; scales based on reminder volume.
- **FR-024**: **Recurring Task Service**:
    - **Core responsibilities**: Manage recurring task definitions, generate new task instances based on schedules.
    - **Public interfaces**: Dapr service invocation.
    - **Events published**: `task-events` (for new task creation), `task-updates`.
    - **Events consumed**: `task-events` (to update recurring task metadata if underlying task changes), `task-updates`.
    - **Dapr APIs used**: Pub/Sub, Scheduled Jobs (for triggering recurrence logic).
    - **Stateless vs stateful classification**: Stateless (recurring task definitions in DB/Dapr State Store).
    - **Horizontal scalability expectations**: Moderate; scales based on number of recurring tasks.
- **FR-025**: **Audit / Activity Log Service**:
    - **Core responsibilities**: Ingest and store all system and user activity events for audit and historical purposes.
    - **Public interfaces**: Dapr service invocation (for direct log entry), Pub/Sub subscription.
    - **Events published**: None.
    - **Events consumed**: `task-events`, `reminders`, `task-updates` (all relevant system events).
    - **Dapr APIs used**: Pub/Sub, State Management (for durable logging if needed), Bindings (for external log storage).
    - **Stateless vs stateful classification**: Stateful (due to log storage).
    - **Horizontal scalability expectations**: High; scales based on event volume.
- **FR-026**: **Real-time Sync Service**:
    - **Core responsibilities**: Distribute task updates to connected clients in real-time.
    - **Public interfaces**: WebSocket.
    - **Events published**: None.
    - **Events consumed**: `task-events`, `task-updates`.
    - **Dapr APIs used**: Pub/Sub.
    - **Stateless vs stateful classification**: Stateless (manages connections, not core data).
    - **Horizontal scalability expectations**: High; scales based on concurrent client connections.

#### Dapr Usage Requirements

- **FR-027**: Dapr MUST be the ONLY integration layer for Pub/Sub (Kafka abstraction).
- **FR-028**: Dapr MUST be the ONLY integration layer for State Management.
- **FR-029**: Dapr MUST be the ONLY integration layer for Service Invocation.
- **FR-030**: Dapr MUST be the ONLY integration layer for Scheduled jobs (Jobs API or Bindings).
- **FR-031**: Dapr MUST be the ONLY integration layer for Secrets management.
- **FR-032**: Direct Kafka client usage in application code is explicitly FORBIDDEN.
- **FR-033**: Direct DB drivers are explicitly FORBIDDEN where Dapr state store is defined.
- **FR-034**: Hardcoded connection strings are explicitly FORBIDDEN.

#### State & Data Management Requirements

- **FR-035**: PostgreSQL (Neon or in-cluster) MUST store core task data, recurring task definitions, and user profiles.
- **FR-036**: Dapr State Store MUST handle conversation state (e.g., chat history, AI context) and potentially transient per-service state.
- **FR-037**: Conversation state handling MUST ensure continuity across chat interactions and be durable.
- **FR-038**: Task state MUST be clearly separated from event history. Task state represents the current facts, while event history represents the changes over time.
- **FR-039**: Data retention and cleanup policies MUST be defined for all data stores (PostgreSQL, Dapr State Store, event logs). Conceptual - e.g., task events retained for 1 year, audit logs for 5 years.

#### Deployment Specification Requirements

- **FR-040**: **Local Deployment (Minikube)**:
    - **Namespaces**: Services MUST be deployed into dedicated Kubernetes namespaces (e.g., `todo-frontend`, `todo-backend`).
    - **Component installation order**: Dapr control plane MUST be installed first, followed by Kafka components, then application services.
    - **Kafka setup approach**: Self-hosted Kafka (e.g., Strimzi or equivalent) within Minikube, or a free serverless tier if applicable for Minikube simulation.
    - **Validation checklist**: Checklist MUST verify all services are running, Dapr sidecars are injected, Kafka topics are created, and basic end-to-end functionality works.
- **FR-041**: **Cloud Deployment (Oracle OKE)**:
    - **Environment parity with local**: The OKE deployment environment MUST be functionally equivalent to the local Minikube setup.
    - **Helm-based deployment assumptions**: Deployment MUST utilize Helm charts for packaging and managing Kubernetes resources.
    - **Config separation (dev vs cloud)**: Configuration MUST be externalized and managed separately for development (local) and cloud environments.
    - **Cost-control principles**: Deployment MUST adhere to always-free tier limitations and minimize resource consumption.

#### CI/CD Pipeline Requirements (GitHub Actions)

- **FR-042**: The CI/CD pipeline MUST be implemented using GitHub Actions (free tier).
- **FR-043**: **Trigger conditions**: Pipeline MUST trigger on push to `main` branch and pull requests for feature branches.
- **FR-044**: **Build stages**: Pipeline MUST include stages for code linting, unit testing, and container image building for each service.
- **FR-045**: **Containerization strategy**: Each service MUST be containerized using Docker, with multi-stage builds for optimized image size.
- **FR-046**: **Kubernetes deployment approach**: Helm charts MUST be used for deploying services to Kubernetes (Minikube for staging/testing, OKE for production).
- **FR-047**: **Rollback philosophy**: The pipeline MUST support automated rollback to the last stable version in case of deployment failure.

#### Security & Resilience Requirements

- **FR-048**: **Secret handling**: Secrets MUST be managed using Kubernetes Secrets and integrated with Dapr Secrets management API.
- **FR-049**: **mTLS via Dapr**: All inter-service communication MUST enforce mTLS via Dapr.
- **FR-050**: **Failure scenarios (Kafka down, service crash)**: The system MUST gracefully handle failures such as Kafka unavailability (Dapr retries) and individual service crashes (Kubernetes restarts, circuit breakers).
- **FR-051**: **Backoff and retry approach**: Services MUST implement exponential backoff and retry mechanisms for transient failures when interacting with external dependencies or other services.
- **FR-052**: **Graceful degradation**: In case of partial system failures (e.g., notification service down), core task functionality MUST remain operational.

#### Observability Requirements

- **FR-053**: **Logging expectations**: All services MUST produce structured logs (e.g., JSON) with correlation IDs for tracing requests.
- **FR-054**: **Minimal metrics**: Each service MUST expose basic metrics (e.g., request count, error rates, latency) for monitoring.
- **FR-055**: **Traceability via event IDs**: All events MUST include a unique `event_id` and `correlation_id` to enable end-to-end traceability across services.
- **FR-056**: **Debugging strategy without paid tools**: The system MUST support effective debugging using open-source tools and techniques (e.g., `kubectl logs`, `port-forward`, distributed tracing with open-source collectors).

### Key Entities *(include if feature involves data)*

- **Task**: Represents a single todo item. Attributes include: `id`, `title`, `description`, `status` (e.g., pending, completed), `priority`, `tags` (array), `dueDate`, `reminderSettings` (object), `recurrencePattern` (object), `userId`, `createdAt`, `updatedAt`.
- **User**: Represents a user of the Todo AI Chatbot. Attributes include: `id`, `username`, `email`, `notificationPreferences` (object).
- **Conversation State**: Transient state for ongoing chat interactions. Attributes include: `userId`, `context` (AI context), `lastInteractionTimestamp`.
- **Event**: Represents a system or user action. Attributes include: `eventId`, `eventType`, `sourceService`, `timestamp`, `payload` (details of the event), `correlationId`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The transformed Todo AI Chatbot application MUST demonstrate 100% functional equivalence to all prior phase functionalities (Basic, Intermediate, Advanced) via the chat interface.
- **SC-002**: The event-driven architecture MUST correctly process 99.9% of `task-events`, `reminders`, and `task-updates` within 500ms under normal load (e.g., 100 concurrent users).
- **SC-003**: Dapr MUST be utilized for all specified integration patterns (Pub/Sub, State, Invocation, Scheduled Jobs, Secrets), with no direct usage of underlying technologies (Kafka clients, direct DB drivers).
- **SC-004**: The deployed solution on Oracle Cloud OKE MUST operate entirely within the always-free tier limits, incurring zero cost for infrastructure.
- **SC-005**: All development artifacts (specs, plans, tasks, code) MUST demonstrably comply with the Agentic Dev Stack methodology, verified through auditing of the repository history.
- **SC-006**: Real-time multi-client awareness MUST ensure task changes are reflected across connected clients within 1 second for 95% of updates.
- **SC-007**: Reminder notifications MUST be successfully delivered for 99% of scheduled reminders.
- **SC-008**: Recurring tasks MUST be generated according to their defined schedules with 99% accuracy.
- **SC-009**: The local Minikube deployment MUST be fully functional and verifiable within 15 minutes.
- **SC-010**: The CI/CD pipeline MUST successfully build, test, and deploy a full update to the OKE environment within 30 minutes.
- **SC-011**: The system MUST maintain availability of core task CRUD functionality (FR-001) at 99.9% even when secondary services (e.g., Notification Service) experience failures.
- **SC-012**: All critical secrets MUST be managed via Kubernetes Secrets and Dapr Secrets, with no hardcoded secrets in application code or configuration.