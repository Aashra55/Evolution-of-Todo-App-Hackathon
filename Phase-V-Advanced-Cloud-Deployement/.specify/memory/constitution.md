<!--
<Sync Impact Report>
Version change: 1.0.0 -> 1.0.1
Modified principles: None
Added sections: None
Removed sections: None
Templates requiring updates: None
Follow-up TODOs: None
</Sync Impact Report>
-->
# Todo AI Chatbot – Phase V (Advanced Cloud Deployment) Constitution

## Core Principles

### I. Free-First Infrastructure
All infrastructure and services MUST be exclusively free-tier or always-free. NO paid services or time-limited credits as hard dependencies are permitted. The project must be completable with zero out-of-pocket cost while maintaining production-grade and judge-ready architecture.

### II. Microservices & Event-Driven Architecture
The system MUST employ a microservices-based, event-driven architecture using Kafka-style messaging. Services are strongly decoupled via Dapr.

### III. Dapr as Abstraction Layer
Dapr MUST be used as the mandatory abstraction layer for Pub/Sub (Kafka-compatible), State Management, Service Invocation, Jobs API/Bindings for scheduled reminders, and Secrets Management. Direct Kafka client libraries are forbidden in application code; all communication with Dapr sidecars MUST use HTTP/gRPC.

### IV. Swappable Infrastructure & Configuration
All infrastructure components MUST be swappable via configuration, with no hardcoding of specific providers or implementations. This includes local (Minikube, Docker, Helm, Redpanda/Strimzi) and cloud (Oracle Cloud OKE, Neon DB/PostgreSQL) deployments.

### V. Spec-Driven Development (SDD)
Development MUST strictly follow the Agentic Dev Stack workflow: 1. Write specification, 2. Generate execution plan, 3. Break into tasks, 4. Implement via agentic code. Manual coding is forbidden as a primary implementation method.

### VI. CI/CD & Secrets Management
Continuous Integration/Continuous Deployment (CI/CD) MUST use GitHub Actions (free tier, public repository). Secrets MUST be managed via Kubernetes Secrets and Dapr `secretstores.kubernetes`.

## Infrastructure Constraints & Non-Goals

*   **Non-Goals:** Explicitly excluded are paid cloud services, reliance on time-limited credits for core functionality, and direct Kafka client library usage within microservices.
*   **Local Development Stack:** Minikube (local Kubernetes), Docker, Helm, Dapr (full installation on Kubernetes), Self-hosted Kafka compatible system (Redpanda or Strimzi Kafka Operator).
*   **Cloud Deployment Stack:** PRIMARY: Oracle Cloud OKE (Always Free - 4 OCPUs, 24GB RAM, no post-trial billing). OPTIONAL (for comparison only): Azure AKS (within free credits).
*   **Kafka/Event Streaming:** PRIMARY: Self-hosted Kafka via Strimzi Operator in Kubernetes. OPTIONAL: Redpanda Cloud Serverless (free tier only). Abstracted via Dapr Pub/Sub.
*   **Database:** Neon DB (Free tier) OR PostgreSQL inside Kubernetes (if needed).
*   **CI/CD:** GitHub Actions (free tier, public repository).
*   **Secrets:** Kubernetes Secrets, Dapr `secretstores.kubernetes`.

## Architectural Guidelines & Deliverables

*   **Microservices:** Frontend Service (Next.js), Chat API Service (FastAPI + MCP tools), Notification Service, Recurring Task Service, WebSocket / Real-time Sync Service (optional).
*   **Dapr Usage:** Pub/Sub, State Management, Service Invocation, Jobs API or Bindings, Secrets Management.
*   **Event-Driven:** Mandatory Kafka Topics: `task-events`, `reminders`, `task-updates`. Event use cases: Task CRUD audit logging, Reminder scheduling & notifications, Recurring task generation, Real-time client sync.
*   **Deployment Phases:**
    *   Phase A: Advanced Features (Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, Sort, Event-driven architecture).
    *   Phase B: Local Kubernetes Deployment (Minikube, Dapr, Kafka deployment, Dapr communication validation).
    *   Phase C: Cloud Deployment (Oracle Cloud OKE, Dapr, in-cluster Kafka, Helm charts, basic monitoring & logging).
*   **Deliverables:** The project will demonstrate a fully functional Todo AI Chatbot adhering to the free-first infrastructure constraint, microservices architecture, Dapr abstraction, and event-driven principles, deployed both locally and in the specified always-free cloud environment. The solution will be judge-ready with clear documentation and adherence to the Spec-Driven Development workflow.

## Governance

This constitution supersedes all other practices and documentation. Amendments require formal documentation, approval by the project lead, and a migration plan for any affected systems or processes. All pull requests and code reviews MUST verify strict compliance with these principles. Complexity introduced MUST be explicitly justified against the "Simplicity" principle. The Agentic Dev Stack workflow described in this constitution is mandatory for all development efforts.

**Version**: 1.0.1 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-09