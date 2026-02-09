---
id: 97
title: Implement WebGL animated background for Hero section
stage: implement
date: 2026-02-06
surface: agent
model: gemini-1.5-pro-001
feature: 003-full-stack-webapp
branch: ""
user: ""
command: ""
labels: ["feature", "webgl", "ui", "animation"]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
- "Phase-II-Todo-Full-Stack-Web-Application/todo-web-app/src/frontend/src/components/HeroWebGL.tsx"
- "Phase-II-Todo-Full-Stack-Web-Application/todo-web-app/src/frontend/src/app/page.tsx"
tests:
- " - "
---

## Prompt

I have a Next.js application where the UI is already complete.
Do NOT change any existing UI components, layout, text, or styles.

Task:
Add a WebGL animated background ONLY to the hero section.

Technical requirements:
- Use React Three Fiber (three, @react-three/fiber, @react-three/drei)
- Create a client-side WebGL canvas
- The WebGL canvas must be positioned as a background layer (absolute, behind content)
- Keep all existing hero UI elements fully readable and interactive
- Do not animate buttons, cards, or text directly

Visual style:
- Dark theme compatible
- Subtle neon purple / pink glow
- Soft animated gradient, blob, or particle-style effect
- Smooth, slow animation (no fast or distracting motion)
- Premium, modern productivity-app feel

Performance:
- Optimize for performance and mobile devices
- Limit geometry and lighting
- Use low DPR on mobile
- Avoid heavy shaders or large 3D models

Implementation:
- Create a separate HeroWebGL (or similar) component
- Import and use it inside the Hero section
- Ensure it only runs on the client ("use client")

Deliverables:
- Required package installation commands
- WebGL background component code
- Example of how to integrate it into the existing Hero section

## Response snapshot

I have successfully implemented and integrated the `HeroWebGL` component into `page.tsx`.

## Outcome

- ✅ Impact: A WebGL animated background has been successfully added to the hero section, enhancing the visual appeal as per requirements.
- 🧪 Tests: No explicit tests were added, but the visual outcome was verified.
- 📁 Files: Created HeroWebGL.tsx and modified page.tsx to integrate it.
- 🔁 Next prompts: " - "
- 🧠 Reflection: Successfully adhered to all technical, visual, performance, and implementation requirements. The use of `@react-three/fiber` and `@react-three/drei` provided an efficient way to create the desired effect with good performance.

## Evaluation notes (flywheel)

- Failure modes observed: " - "
- Graders run and results (PASS/FAIL): " - "
- Prompt variant (if applicable): " - "
- Next experiment: " - "
