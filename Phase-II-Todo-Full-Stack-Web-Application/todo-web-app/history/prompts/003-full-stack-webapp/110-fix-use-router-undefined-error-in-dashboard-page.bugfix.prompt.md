---
phr_id: 110
phr_title: Fix useRouter undefined error in dashboard page
phr_stage: bugfix
phr_date_iso: 2026-02-07
phr_surface: agent
phr_model: claude-3-opus
phr_feature: full-stack-webapp
phr_branch: main
phr_user: user
phr_command: None
phr_labels: ["nextjs", "frontend", "bugfix"]
phr_links:
  spec: null
  ticket: null
  adr: null
  pr: null
phr_files_yaml:
  - src/frontend/src/app/dashboard/page.tsx
phr_tests_yaml: []
phr_prompt_text: |-
  Error:Runtime ReferenceError



  useRouter is not defined
  src/app/dashboard/page.tsx (16:18) @ Dashboard


    14 |
    15 | export default function Dashboard() {
  > 16 |   const router = useRouter();
       |                  ^
    17 |   const [tasks, setTasks] = useState<Task[]>([]);
    18 |   const [error, setError] = useState<string | null>(null);
    19 |
  Call Stack
  13

  Show 12 ignore-listed frame(s)
  Dashboard
  src/app/dashboard/page.tsx (16:18)
phr_response_text: |-
  I have re-added the `useRouter` import to `src/frontend/src/app/dashboard/page.tsx`. This should resolve the `useRouter is not defined` error.

  I should now update the PHR to reflect this correction.
---
