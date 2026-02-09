<!--
  Sync Impact Report
  Version change: 0.0.0 → 1.0.0
  List of modified principles:
    - I. Vision and Purpose (Added)
    - II. Agentic-First Development (Added)
    - III. Model Context Protocol (MCP) Centricity (Added)
    - IV. Statelessness and Persistence (Added)
    - V. Secured Data Access (Added)
    - VI. Mandatory Technology Stack (Added)
  Added sections:
    - Development Workflow and Compliance
    - Non-Functional Requirements & Success Criteria
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md: ⚠ pending (Constitution Check section needs review for alignment with new principles)
    - .specify/templates/spec-template.md: ⚠ pending (Scope/requirements alignment with new principles)
    - .specify/templates/tasks-template.md: ⚠ pending (Task categorization with new principle-driven task types)
    - .gemini/commands/sp.adr.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.analyze.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.checklist.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.clarify.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.constitution.toml: ✅ updated (This file itself)
    - .gemini/commands/sp.git.commit_pr.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.implement.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.phr.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.plan.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.reverse-engineer.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.specify.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.tasks.toml: ✅ updated (No outdated references found)
    - .gemini/commands/sp.taskstoissues.toml: ✅ updated (No outdated references found)
    - GEMINI.md: ⚠ pending (This file, as a runtime guidance document, needs review to ensure consistency with the new MCP-centric and agentic development principles).
  Follow-up TODOs: None
-->
# Todo AI Chatbot Constitution

## Core Principles

### I. Vision and Purpose
To build an AI-powered conversational interface for managing todos using natural language, providing a seamless and intuitive user experience.

### II. Agentic-First Development
All development and implementation must be conducted exclusively through agentic workflows, adhering strictly to the Agentic Dev Stack: Write Spec, Generate Plan, Break into Tasks, Implement via AI Agents. Manual coding is prohibited.

### III. Model Context Protocol (MCP) Centricity
The system architecture must leverage the Model Context Protocol (MCP) server. AI agents shall interact with todo operations solely via MCP tools. All MCP tools must be stateless.

### IV. Statelessness and Persistence
The chat endpoint must be stateless. No state shall be stored in memory between requests by any component. All conversational and todo-related state must be persisted exclusively in the designated database.

### V. Secured Data Access
AI agents are strictly prohibited from direct database access. The MCP server is the sole conduit for task operations, exposing them strictly as tools. Security, scalability, and correctness are paramount considerations in all design and implementation decisions.

### VI. Mandatory Technology Stack
Adherence to the defined technology stack is mandatory: Frontend (OpenAI ChatKit), Backend (Python FastAPI), AI Framework (OpenAI Agents SDK), MCP Server (Official MCP SDK), ORM (SQLModel), Database (Neon Serverless PostgreSQL), Authentication (Better Auth).

## Development Workflow and Compliance

*   **Agentic Development Stack:** Strict adherence to the Agentic Dev Stack is required:
    1.  Write Specification: Define features and requirements in a clear, unambiguous spec.
    2.  Generate Plan: Create a detailed architectural and implementation plan from the spec.
    3.  Break into Tasks: Decompose the plan into granular, testable tasks.
    4.  Implement via AI Agents: Execute tasks through agentic code generation and modification.
*   **Review and Grading:** All development processes, prompts, iterations, and architectural decisions are subject to review and grading. Deviations from this workflow are considered violations.
*   **Do's and Don'ts:**
    *   **Do:** Prioritize natural language understanding for todo management. Ensure all MCP tools are stateless. Persist all conversation state in the database. Ensure security, scalability, and correctness are first-class concerns.
    *   **Don't:** Allow manual coding. Permit direct database access by AI agents. Store state in memory between requests. Introduce components outside the mandatory technology stack.

## Non-Functional Requirements & Success Criteria

*   **Non-Functional Requirements:**
    *   **Security:** Robust authentication and authorization via Better Auth. Secure handling of all data. No secrets hardcoded or exposed.
    *   **Scalability:** The system must be capable of handling increasing user loads and data volumes. Stateless design promotes horizontal scaling.
    *   **Correctness:** All todo operations performed via the AI conversational interface must be accurate and reliable.
    *   **Performance:** Responses from the chatbot should be timely and efficient for a smooth user experience.
    *   **Observability:** Comprehensive logging, metrics, and tracing for monitoring system health and debugging.
*   **Success Criteria:**
    *   Successful implementation of all core functional requirements outlined in the specifications.
    *   Strict adherence to the Agentic Dev Stack and all constitutional principles.
    *   High user satisfaction with the natural language interface for todo management.
    *   System stability, security, and performance meeting defined benchmarks.
    *   Positive review and grading of the development process and artifacts.

## Governance

This Constitution serves as the foundational governance document for the Todo AI Chatbot project. All practices and decisions must align with its principles.
Amendments require a formal proposal, justification, impact assessment, and approval by project architects.
Version bumping for this Constitution shall follow semantic versioning (MAJOR.MINOR.PATCH).
Compliance with this Constitution will be regularly reviewed, with findings reported to project leadership.
The `GEMINI.md` file contains additional runtime guidance for agent development and must be consulted for specific operational instructions.

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07