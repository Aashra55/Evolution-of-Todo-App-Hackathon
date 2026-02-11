---
id: 28
title: Finalized Chat and Task Panel Border Removal
stage: green
date: 2026-02-11
surface: agent
model: gemini-1.5-flash
feature: todo-ai-chatbot
branch: main
user: user
command: Finalize chat section and task panel border removal
labels: [ui, css, frontend, bugfix]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/styles/custom-neon.css
tests: []
prompt_text: |-
  GEMINI.md main ss paste kia h mene dekho chat section k borders remove nh huye hain or na hi koi background show horaha h
response_text: |-
  I have removed the `border-color` property from the `.neon-glow-secondary` class in `custom-neon.css`. This should finally resolve the persistent border issue for both the chat section and the task panel, as `chat-display-wrapper` and `task-panel-wrapper` already contain `border: none;` and background styling.
---

## Finalized Chat and Task Panel Border Removal and Background Application

This change directly addresses the persistent issue of borders appearing on the chat section and task panel, as identified by the user's screenshot. The core problem was the `border-color` property within the `.neon-glow-secondary` class, which was overriding `border: none;` declarations in other wrapper classes due to CSS specificity or cascade order.

### Changes Made:

1.  **`frontend/src/styles/custom-neon.css`**: The `border-color: var(--color-neon-secondary);` property was removed from the `.neon-glow-secondary` class definition.

This modification ensures that any element utilizing `.neon-glow-secondary` will now only receive the `box-shadow` effect without an accompanying border. Consequently, the `border: none;` rules in `.chat-display-wrapper` and `.task-panel-wrapper` (which also define the light backgrounds) will now correctly take effect, finally achieving the user's desired borderless appearance and distinct light backgrounds for both the chat display and task panel.
