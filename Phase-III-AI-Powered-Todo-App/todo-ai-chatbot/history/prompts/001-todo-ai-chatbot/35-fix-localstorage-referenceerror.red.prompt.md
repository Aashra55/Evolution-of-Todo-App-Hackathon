---
id: 35
title: Fix localStorage ReferenceError and hydration issues
stage: red
date: 2026-02-21
surface: agent
model: gemini-2.0-flash
feature: 001-todo-ai-chatbot
branch: main
user: Me
command: fix the error: Server Error ReferenceError: localStorage is not defined
labels: ["fix", "ssr", "nextjs", "authentication"]
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - frontend/src/services/authService.js
  - frontend/src/components/App.js
tests_yaml:
  - null
prompt_text: |
  fix the error: Server Error
  ReferenceError: localStorage is not defined

  This error happened while generating the page. Any console logs will be displayed in the terminal window.
  Source
  src\services\authService.js (41:4) @ Object.getAccessToken

    39 |
    40 | getAccessToken() {
  > 41 |   return localStorage.getItem('access_token');
       |  ^
    42 | },
    43 |
    44 | isAuthenticated() {
  Call Stack
  getAccessToken
  src\services\authService.js (45:18)
  authService
  src\components\App.js (174:7)
  Show collapsed frames
response_text: |
  I've fixed the `ReferenceError: localStorage is not defined` and potential hydration issues in the frontend.

  Summary of changes:
  1.  **`frontend/src/services/authService.js`**: Added checks for `typeof window !== 'undefined'` before accessing `localStorage` to ensure compatibility with server-side rendering (SSR).
  2.  **`frontend/src/components/App.js`**: 
      - Introduced an `isReady` state to track when the client-side hydration and authentication checks are complete.
      - Updated the `useEffect` hook to set `isReady` to `true` after performing the initial authentication check.
      - Deferred rendering the main application UI until `isReady` is `true`, preventing SSR from trying to access client-only data or APIs.
      - Restored the `handleSendMessage` function.
outcome: success
evaluation: The changes correctly handle the absence of browser APIs during server-side rendering, which is the root cause of the reported error.
---
