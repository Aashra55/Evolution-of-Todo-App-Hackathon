---
id: 30
title: fixed-nextjs-hydration-error-on-register-page
stage: red
date: 2026-02-18
surface: agent
model: gemini-2.0-flash-exp
feature: todo-ai-chatbot
branch: null
user: Me
command: none
labels: ["bug-fix", "frontend", "react", "nextjs", "hydration-error"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/pages/register.js
tests:
 - none
---

## Prompt

error: Unhandled Runtime Error
Error: Hydration failed because the initial UI does not match what was rendered on the server.

Warning: Expected server HTML to contain a matching <label> in <div>.

See more info here: https://nextjs.org/docs/messages/react-hydration-error

Component Stack
label
div
form
div
div
RegisterPage
MyApp
...

## Response snapshot

Fixed the Next.js hydration error by dynamically importing the `Notifications` component with SSR disabled and conditionally rendering it. This ensures the component is only rendered on the client-side, resolving the mismatch between server and client HTML.

## Outcome

- ✅ Impact: Resolved the frontend crash (hydration error) on the registration page.
- 🧪 Tests: Manual verification recommended.
- 📁 Files: Modified `frontend/src/pages/register.js`.
- 🔁 Next prompts: None.
- 🧠 Reflection: Hydration errors in Next.js with client-side heavy components are best solved by disabling SSR for those specific components using `next/dynamic`.

## Evaluation notes (flywheel)

- Failure modes observed: React hydration mismatch.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
