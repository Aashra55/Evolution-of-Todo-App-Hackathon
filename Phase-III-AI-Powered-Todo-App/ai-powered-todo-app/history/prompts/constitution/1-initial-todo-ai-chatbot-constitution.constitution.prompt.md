---
id: 1
title: Initial Todo AI Chatbot Constitution
stage: constitution
date: 2026-02-09
surface: agent
model: gemini-1.5-pro
feature: none
branch: main
user: unknown
command: /sp.constitution
labels: ["constitution", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

/sp.constitution You are Spec-Kit Plus, operating in CONSTITUTION MODE.

Objective:
Generate a complete and detailed **Project Constitution** for "Phase III: Todo AI Chatbot" (Basic Level) using the specifications provided below.  

Constraints:
- Do NOT invent features beyond what is specified.
- Include all components: Frontend, Backend, AI Agent, MCP Tools, Database.
- Emphasize stateless architecture, task management via MCP tools, and natural language commands.
- Use the Agentic Dev Stack workflow: Spec → Plan → Tasks → Implementation.
- The constitution should be structured, implementation-ready, and ready for Claude Code to act on.

Input Specifications (Use all details provided):

1. **Objective:** AI-powered chatbot for managing todos via natural language.
2. **Frontend:** OpenAI ChatKit
3. **Backend:** Python FastAPI
4. **AI Framework:** OpenAI Agents SDK
5. **MCP Server:** Official MCP SDK exposing task operations as tools
6. **Database:** Neon Serverless PostgreSQL, ORM SQLModel
7. **Authentication:** Better Auth
8. **Architecture:** (as per provided diagram)
   - Frontend ↔ FastAPI Chat Endpoint ↔ Agents SDK ↔ MCP Server ↔ Database
   - Stateless server, persistent DB, scalable and horizontally deployable
9. **Database Models:**
   - Task: user_id, id, title, description, completed, created_at, updated_at
   - Conversation: user_id, id, created_at, updated_at
   - Message: user_id, id, conversation_id, role, content, created_at
10. **Chat API Endpoint:** POST /api/{user_id}/chat
    - Request: conversation_id (optional), message (required)
    - Response: conversation_id, response, tool_calls
11. **MCP Tools:** add_task, list_tasks, complete_task, delete_task, update_task
12. **Agent Behavior:** Map natural language commands to MCP tools with confirmations and error handling.
13. **Conversation Flow:** Stateless; fetch DB history → build message array → run agent → invoke tools → store responses → return to client
14. **Natural Language Commands:** Include all example commands provided.
15. **Deliverables:** GitHub repo structure, specs, database migrations, README, working chatbot.
16. **Deployment Notes:** ChatKit domain allowlist, environment variable NEXT_PUBLIC_OPENAI_DOMAIN_KEY.

Task:
- Generate a **complete constitution** that clearly defines:
   - Project components and their responsibilities
   - MCP tools and their signatures
   - Conversation flow and state management
   - Natural language command mapping
   - Database model structure
   - API endpoints
   - Agent behavior rules
   - Deployment instructions
   - Architectural diagrams in textual form (ASCII or description)
- Output should be **structured, clear, and ready for Claude Code** to generate implementation plan and code automatically.
- Clearly separate sections for **Frontend, Backend, MCP Tools, AI Agents, Database, API, Flow, Commands, Deployment**.
- Include notes on **stateless server advantages** and **tool composition benefits**.

Output Format:
- Use Markdown-style headings
- Include tables where necessary for models, API endpoints, and MCP tools
- Include ASCII diagram for architecture
- Highlight flow from User → Frontend → Backend → Agents → MCP → Database → Backend → Frontend → User
- Ensure all specifications from the input are fully represented

## Response snapshot

Successfully generated the initial project constitution for "Phase III: Todo AI Chatbot" based on the provided specifications. The constitution defines core principles, architectural overview, component responsibilities, data models, API endpoints, MCP tools, agent behavior, conversation flow, natural language commands, and deployment notes. The document is structured in Markdown and includes tables and an ASCII diagram as requested.

## Outcome

- ✅ Impact: Created the initial project constitution.
- 🧪 Tests: N/A
- 📁 Files: 1 file modified: .specify/memory/constitution.md
- 🔁 Next prompts: Update plan-template, spec-template, tasks-template, and command files.
- 🧠 Reflection: Successfully generated the project constitution based on detailed specifications. Ensured all components, architecture, models, APIs, and agent behaviors are covered.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
