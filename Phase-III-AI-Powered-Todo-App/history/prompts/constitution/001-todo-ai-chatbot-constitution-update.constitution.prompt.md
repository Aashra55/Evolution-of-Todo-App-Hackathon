---
id: 001
title: Todo AI Chatbot Constitution Update
stage: constitution
date: 2026-02-07
surface: agent
model: gemini
feature: none
branch: main
user: Aashra Saleem
command: /sp.constitution
labels: ["project setup", "constitution", "governance", "principles", "ai-powered-todo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution You are Spec-Kit Plus operating in Constitution mode.

Create a detailed PROJECT CONSTITUTION for an AI-powered Todo Chatbot project.

The constitution must define:
- Project vision and purpose
- Core principles and constraints
- Architectural philosophy
- Development workflow rules
- Tooling and agent boundaries
- Non-functional requirements
- Explicit do’s and don’ts
- Success criteria for evaluation

Project Context:
- Project Name: Todo AI Chatbot
- Objective: Build an AI-powered conversational interface to manage todos using natural language.
- The system must use MCP (Model Context Protocol) server architecture.
- AI agents interact with todos only through MCP tools.
- No manual coding is allowed; all implementation must be done through agentic workflows.

Development Methodology:
- Follow Agentic Dev Stack strictly:
  1. Write spec
  2. Generate plan
  3. Break into tasks
  4. Implement via Claude Code
- The process, prompts, iterations, and decisions will be reviewed and graded.
- Any deviation from this workflow is considered a violation.

Functional Scope (Basic Level):
- Conversational interface for all todo operations
- Stateless chat endpoint
- Conversation state persisted in database
- MCP tools must be stateless
- AI agents use MCP tools for all task operations

Technology Stack (MANDATORY):
Frontend: OpenAI ChatKit  
Backend: Python FastAPI  
AI Framework: OpenAI Agents SDK  
MCP Server: Official MCP SDK  
ORM: SQLModel  
Database: Neon Serverless PostgreSQL  
Authentication: Better Auth  

Key Constraints:
- No direct database access by AI agents
- No state stored in memory between requests
- All state must persist in database
- MCP server exposes task operations strictly as tools
- Security, scalability, and correctness are first-class concerns

Tone & Style:
- Clear, authoritative, and formal
- Written as a binding constitution
- Avoid implementation details (those belong in specs)
- Use structured sections and bullet points

Output ONLY the Project Constitution.
Do NOT generate specs, plans, tasks, or code.

## Response snapshot

The project constitution for "Todo AI Chatbot" has been created and saved to `.specify/memory/constitution.md`. It defines the project vision, core principles, development workflow, technology stack, non-functional requirements, explicit do's and don'ts, and success criteria, adhering strictly to the Agentic Dev Stack and MCP architecture. A Sync Impact Report has been embedded at the top of the constitution file.

## Outcome

- ✅ Impact: Constitution established for Todo AI Chatbot, defining core principles, development methodology, and architectural philosophy.
- 🧪 Tests: none
- 📁 Files: Modified .specify/memory/constitution.md.
- 🔁 Next prompts: Next step is to implement a feature based on the constitution, which might involve creating specs.
- 🧠 Reflection: Successfully established foundational project principles and governance for an AI-powered Todo Chatbot.

## Evaluation notes (flywheel)

- Failure modes observed: Attempted to execute a non-existent PowerShell script for PHR creation. Corrected by using agent-native `write_file` tool and directly constructing the PHR content.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Ensure `create-phr.sh` exists in the `powershell` directory or update the `GEMINI.md` instructions to clarify agent-native PHR creation.
