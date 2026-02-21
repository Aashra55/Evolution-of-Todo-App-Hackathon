---
id: 34
title: Fix task identification by name
stage: green
date: 2026-02-21
surface: agent
model: gemini-2.0-flash
feature: 001-todo-ai-chatbot
branch: main
user: Me
command: fix task identification by name
labels: ["fix", "mcp-tools", "task-management"]
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - backend/src/mcp_tools/utils.py
  - backend/src/mcp_tools/complete_task.py
  - backend/src/mcp_tools/delete_task.py
  - backend/src/mcp_tools/update_task.py
  - backend/src/agent/agent_logic.py
tests_yaml:
  - backend/tests/unit/mcp_tools/test_mcp_tools.py
prompt_text: |
  ek issue araha h k task ko delete or complete krwane k liye id batani pad rahi h, task k name se agent task ko delete or mark as completed nh kar paraha h, is issue ko fix karo
response_text: |
  I've fixed the issue where the agent required a task ID for deletion or completion. Now, the agent can identify tasks by name (case-insensitive and partial matching) as well.

  Summary of changes:
  1. Created a `find_task` utility in `backend/src/mcp_tools/utils.py` to handle task lookup by ID or name.
  2. Updated `complete_task`, `delete_task`, and `update_task` tools to use the new utility and accept an optional `task_name` parameter.
  3. Updated the tool schemas to include `task_name` and mark `task_id` as optional.
  4. Updated the AI system prompt in `backend/src/agent/agent_logic.py` to inform the agent that it can now identify tasks by name.
  5. Added and verified unit tests in `backend/tests/unit/mcp_tools/test_mcp_tools.py` for task identification by name.
outcome: success
evaluation: The unit tests confirm that tasks can now be completed, deleted, and updated using their names.
---
