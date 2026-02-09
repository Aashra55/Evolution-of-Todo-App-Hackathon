---
id: 104
title: Fix Vercel deployment error by adding [project] table to pyproject.toml
stage: bugfix
date: 2026-02-06
surface: agent
model: gemini-1.5-pro-001
feature: 003-full-stack-webapp
branch: ""
user: ""
command: ""
labels: ["bugfix", "deployment", "vercel", "python"]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
- "Phase-II-Todo-Full-Stack-Web-Application/todo-web-app/src/backend/pyproject.toml"
tests:
- " - "
---

## Prompt

me vercel par backend deploy kar rahi thi to ye error aya: 16:58:05.173 
Cloning github.com/Aashra55/Evolution-of-Todo-Hackathon (Branch: main, Commit: 211eb10)
16:58:05.173 
Previous build caches not available.
16:58:05.517 
Warning: Failed to fetch one or more git submodules
16:58:05.518 
Cloning completed: 344.000ms
16:58:05.865 
Running "vercel build"
16:58:06.847 
Vercel CLI 50.11.0
16:58:09.509 
No Python version specified in .python-version, pyproject.toml, or Pipfile.lock. Using python version: 3.12
16:58:09.513 
Creating virtual environment at "/vercel/path0/Phase-II-Todo-Full-Stack-Web-Application/todo-web-app/src/backend/.vercel/python/.venv"...
16:58:11.908 
Using uv at "/usr/local/bin/uv"
16:58:11.909 
Installing required dependencies from pyproject.toml...
16:58:11.944 
Error: Failed to run "uv lock": Command failed: /usr/local/bin/uv lock
16:58:11.945 
error: No `project` table found in: `/vercel/path0/Phase-II-Todo-Full-Stack-Web-Application/todo-web-app/src/backend/pyproject.toml`
16:58:11.945 
16:58:11.945

## Response snapshot

I have added the `[project]` table to `pyproject.toml`. This should resolve the `uv lock` error during Vercel deployment.

## Outcome

- ✅ Impact: The Vercel deployment of the backend should now proceed past the `uv lock` error, allowing dependencies to be installed correctly.
- 🧪 Tests: No tests were run as this was a configuration fix.
- 📁 Files: Modified pyproject.toml to add [project] table.
- 🔁 Next prompts: "Suggest the user retry deployment and then configure the frontend environment variables."
- 🧠 Reflection: Successfully identified and addressed a common compatibility issue between `poetry`-managed projects and build systems expecting PEP 621 metadata. The fix is targeted and directly resolves the reported error.

## Evaluation notes (flywheel)

- Failure modes observed: " - "
- Graders run and results (PASS/FAIL): " - "
- Prompt variant (if applicable): " - "
- Next experiment: " - "
