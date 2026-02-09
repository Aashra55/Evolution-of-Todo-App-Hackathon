<!--
Sync Impact Report:
Version change: none -> 0.1.0
List of modified principles:
  - Core Development Philosophy
  - Mandatory Workflow Rules
  - Technology Constraints
  - Infrastructure Rules
  - AIOps Principles
  - Learning & Research Orientation
Added sections:
  - Security & Governance
  - Failure Handling
Removed sections: none
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending (Significant updates needed to reflect AI-driven development and strict automation. Emphasis on AI agent roles and automated generation in technical context and project structure.)
  - .specify/templates/spec-template.md: ⚠ pending (Specifications need to be explicit and detailed enough for AI agent consumption, particularly in user scenarios and requirements.)
  - .specify/templates/tasks-template.md: ⚠ pending (Task categorization and descriptions must reflect AI agent responsibilities and automated execution, e.g., "AI agent generates X", "kubectl-ai deploys Y".)
  - .gemini/commands/sp.adr.toml: ✅ updated
  - .gemini/commands/sp.analyze.toml: ✅ updated
  - .gemini/commands/sp.checklist.toml: ✅ updated
  - .gemini/commands/sp.clarify.toml: ✅ updated
  - .gemini/commands/sp.constitution.toml: ✅ updated
  - .gemini/commands/sp.git.commit_pr.toml: ✅ updated
  - .gemini/commands/sp.implement.toml: ✅ updated
  - .gemini/commands/sp.phr.toml: ✅ updated
  - .gemini/commands/sp.plan.toml: ✅ updated
  - .gemini/commands/sp.reverse-engineer.toml: ✅ updated
  - .gemini/commands/sp.specify.toml: ✅ updated
  - .gemini/commands/sp.tasks.toml: ✅ updated
  - .gemini/commands/sp.taskstoissues.toml: ✅ updated
Follow-up TODOs: none
-->
# Cloud-Native Todo Chatbot — Phase IV: Local Kubernetes Deployment Constitution

## Core Principles

### I. Core Development Philosophy
Spec → Plan → Tasks → Implementation. No direct or manual coding by humans. All implementation MUST be performed by AI agents (Claude Code, Docker AI Agent / Gordon, kubectl-ai, kagent). Human role is review, validation, and approval only.

### II. Mandatory Workflow Rules
Every change MUST originate from a written specification. No Dockerfile, Helm chart, Kubernetes manifest, or command may be written manually. All infrastructure operations MUST be generated via: Claude Code, Docker AI Agent (Gordon) where available, kubectl-ai, kagent. Any deviation from this workflow is considered a violation of the constitution.

### III. Technology Constraints
Containerization: Docker (Docker Desktop). Docker AI: Docker AI Agent (Gordon) preferred. Orchestration: Kubernetes (Minikube only). Package Management: Helm Charts. AI DevOps Agents: kubectl-ai (required), kagent (recommended for advanced analysis). Application Base: Existing Phase III Todo Chatbot.

### IV. Infrastructure Rules
Frontend and backend MUST be containerized separately. Helm charts MUST be used for all Kubernetes deployments. Local-only deployment (no cloud providers). Minikube is the single Kubernetes target. Resource usage should be reasonable for local development.

### V. AIOps Principles
Docker AI Agent (Gordon) is responsible for: Container build strategy, Image optimization, Runtime decisions. kubectl-ai is responsible for: Deployments, Scaling, Debugging failing pods. kagent is responsible for: Cluster health analysis, Resource optimization. If Gordon is unavailable, Claude Code may generate Docker commands instead.

### VI. Learning & Research Orientation
This phase serves as an educational, zero-cost, local DevOps learning environment. Encourage explainability of AI-generated decisions. Support future extension into Spec-Driven Infrastructure Blueprints.

## Security & Governance

Treat all repositories as private. No hardcoded secrets. Follow least-privilege principles. Clear separation of frontend and backend concerns.

## Failure Handling

Any ambiguous instruction MUST result in a clarification step before execution. Silent assumptions are forbidden.

## Governance
This constitution is the supreme governing document for the project. All technical work and process execution MUST adhere strictly to the principles and rules defined herein. Any deviation is considered a violation. Amendments require formal documentation, approval, and a migration plan. Compliance reviews will be conducted regularly.

**Version**: 0.1.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-09