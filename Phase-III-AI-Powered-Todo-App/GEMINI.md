# Todo AI Chatbot Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-07

## Active Technologies

- Python 3.10+ + FastAPI
- OpenAI Agents SDK
- Official MCP SDK
- SQLModel
- Better Auth
- OpenAI ChatKit
- Neon Serverless PostgreSQL

## Project Structure

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

ai-agent/
├── src/
│   └── agents/
└── tests/
```

## Commands

- Python: `cd backend; pytest; ruff check .`
- Frontend: `cd frontend; npm test; npm run lint` (Placeholder - specific commands TBD)
- AI Agent: `cd ai-agent; pytest` (Placeholder - specific commands TBD)
- Run Backend: `cd backend; uvicorn main:app --reload`

## Code Style

Python: Follow standard conventions.

## Recent Changes

- `001-todo-ai-chatbot-basic`: Added Python 3.10+, FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Better Auth, OpenAI ChatKit, Neon Serverless PostgreSQL

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->