# Implementation Plan: Todo AI Chatbot Phase V - Advanced Cloud Deployment

**Branch**: `002-phase-v-spec` | **Date**: 2026-02-09 | **Spec**: [specs/002-phase-v-spec/spec.md](specs/002-phase-v-spec/spec.md)
**Input**: Feature specification from `specs/002-phase-v-spec/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The core objective of Phase V is to transform the existing Todo AI Chatbot from a CRUD-based application into a production-style, event-driven, agentic microservices system. This will involve re-architecting the application using Kubernetes for orchestration, Kafka-style messaging for inter-service communication (abstracted by Dapr), and Dapr as the mandatory abstraction layer for Pub/Sub, State Management, Service Invocation, Scheduled Jobs/Bindings, and Secrets Management. The entire solution MUST adhere to a free-first infrastructure principle and the Spec-Driven Development (SDD) methodology.

## Technical Context

**Language/Version**: Python 3.11+ (for FastAPI services), JavaScript/TypeScript (Node.js 18+ for Next.js Frontend)  
**Primary Dependencies**: FastAPI, Next.js, Dapr (sidecars and control plane), Kubernetes (Minikube/OKE), Kafka-style messaging (Strimzi/Redpanda), PostgreSQL.  
**Storage**: PostgreSQL (Neon or in-cluster) for core task data, recurring task definitions, user profiles. Dapr State Store (e.g., Redis or PostgreSQL via Dapr state component) for conversation state and transient per-service state.  
**Testing**: Pytest (for Python services), Jest/React Testing Library (for Next.js Frontend for unit/component tests), Playwright (for E2E tests).  
**Target Platform**: Kubernetes (Minikube for local development, Oracle Cloud OKE for cloud deployment). Web browsers for Frontend access.  
**Project Type**: Distributed Microservices Architecture (Frontend, Chat API, Notification, Recurring Task, Audit/Activity Log, Real-time Sync Services).  
**Performance Goals**: The event-driven architecture MUST correctly process 99.9% of `task-events`, `reminders`, and `task-updates` within 500ms under normal load (e.g., 100 concurrent users). Real-time multi-client awareness MUST ensure task changes are reflected across connected clients within 1 second for 95% of updates.  
**Constraints**:
- ALL infrastructure MUST be free-tier or always-free. NO paid services or time-limited credits.
- Development MUST strictly follow the Agentic Dev Stack workflow (spec-first, plan, tasks, agentic implementation only).
- Dapr MUST be the ONLY integration layer for Pub/Sub, State Management, Service Invocation, Scheduled Jobs/Bindings, and Secrets Management. Direct Kafka client usage and direct DB drivers (where Dapr state store is defined) are FORBIDDEN.
- Hardcoded connection strings are FORBIDDEN.
- CI/CD MUST use GitHub Actions (free tier).
**Scale/Scope**: Implementation of all prior-level functionality (Basic, Intermediate, Advanced) within an event-driven microservices architecture composed of six distinct services, deployed both locally (Minikube) and to Oracle Cloud OKE.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [X] **I. Free-First Infrastructure**: All infrastructure and services MUST be exclusively free-tier or always-free.
- [X] **II. Microservices & Event-Driven Architecture**: The system MUST employ a microservices-based, event-driven architecture using Kafka-style messaging. Services are strongly decoupled via Dapr.
- [X] **III. Dapr as Abstraction Layer**: Dapr MUST be used as the mandatory abstraction layer for Pub/Sub, State Management, Service Invocation, Jobs API/Bindings, and Secrets Management. Direct Kafka client libraries are forbidden.
- [X] **IV. Swappable Infrastructure & Configuration**: All infrastructure components MUST be swappable via configuration, with no hardcoding of specific providers.
- [X] **V. Spec-Driven Development (SDD)**: Development MUST strictly follow the Agentic Dev Stack workflow. Manual coding is forbidden as a primary implementation method.
- [X] **VI. CI/CD & Secrets Management**: CI/CD MUST use GitHub Actions (free tier, public repository). Secrets MUST be managed via Kubernetes Secrets and Dapr secretstores.kubernetes.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-v-spec/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── lib/
└── tests/

services/
├── chat-api/
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   └── services/
│   └── tests/
├── notification/
│   ├── src/
│   │   ├── models/
│   │   └── services/
│   └── tests/
├── recurring-task/
│   ├── src/
│   │   ├── models/
│   │   └── services/
│   └── tests/
├── audit-log/
│   ├── src/
│   │   ├── models/
│   │   └── services/
│   └── tests/
├── real-time-sync/
│   ├── src/
│   │   ├── models/
│   │   └── services/
│   └── tests/

```

**Structure Decision**: The project will adopt a multi-service structure, with a top-level `frontend` directory for the Next.js application and a `services` directory containing separate sub-directories for each backend microservice (Chat API, Notification, Recurring Task, Audit Log, Real-time Sync). Each service directory will contain its `src/` and `tests/` folders. This aligns with a microservices approach, clearly separating concerns and facilitating independent development and deployment.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| | | |