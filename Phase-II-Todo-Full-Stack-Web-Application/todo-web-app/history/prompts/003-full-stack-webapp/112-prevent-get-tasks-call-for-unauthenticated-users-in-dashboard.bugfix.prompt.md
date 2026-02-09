---
phr_id: 112
phr_title: Prevent getTasks call for unauthenticated users in dashboard
phr_stage: bugfix
phr_date_iso: 2026-02-07
phr_surface: agent
phr_model: claude-3-opus
phr_feature: full-stack-webapp
phr_branch: main
phr_user: user
phr_command: None
phr_labels: ["nextjs", "frontend", "bugfix", "authentication"]
phr_links:
  spec: null
  ticket: null
  adr: null
  pr: null
phr_files_yaml:
  - src/frontend/src/app/dashboard/page.tsx
phr_tests_yaml: []
phr_prompt_text: |-
  Error: Console Error

  No authentication token found
  src/services/api.ts (41:11) @ getAuthHeaders
phr_response_text: |-
  I have fixed the issue where `getTasks()` was called even when the user was not authenticated, leading to the "No authentication token found" error. The `useEffect` now correctly returns if the user is not authenticated, preventing the API call.

  I will now update the PHR to reflect this correction.
---
