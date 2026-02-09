# Cloud-Native Todo Chatbot — Phase IV: Local Kubernetes Deployment

This project represents Phase IV of the Cloud-Native Todo Chatbot, focusing on deploying the application locally using Minikube, Docker, and Helm, driven by AI agents.

## Project Overview

The Cloud-Native Todo Chatbot — Phase IV aims to provide a fully containerized and orchestrated local development environment. This phase emphasizes Spec-Driven Development principles, where AI agents are responsible for generating specifications, plans, tasks, Docker images, Helm charts, and managing the Kubernetes deployment on Minikube. Human involvement is limited to review, validation, and approvals.

## Features

This phase focuses on the *deployment and orchestration* aspects, demonstrating the capabilities of AI agents in a cloud-native context:

*   **Local Kubernetes Deployment**: Deploying the application stack on a local Minikube cluster.
*   **Containerization**: Separately containerizing frontend and backend applications.
*   **AI-Assisted Container Building**: Utilizing Docker AI Agent (Gordon) for intelligent image creation and optimization.
*   **AI-Generated Helm Charts**: Generating and managing Kubernetes deployment configurations using Helm charts created by AI.
*   **AI-Orchestrated Deployment**: Deploying applications via `kubectl-ai` and managing the cluster with `kagent`.
*   **Scalability, Observability, Reliability**: Ensuring these aspects are considered in the local deployment strategy.
*   **AI-Assisted Management**: Implementing debugging, scaling, and health monitoring via AI agents.
*   **Spec-Driven Development**: All artifacts (specs, plans, tasks, code, configs) generated and managed via AI based on initial specifications.

## Tech Stack

*   **Frontend**: React (TypeScript)
*   **Backend**: Node.js (TypeScript), Express.js
*   **Database**: PostgreSQL
*   **Containerization**: Docker
*   **Orchestration**: Kubernetes (Minikube)
*   **Deployment**: Helm Charts
*   **AI Agents**: Docker AI Agent (Gordon), Claude Code, `kubectl-ai`, `kagent`

## Project Structure

The project follows a monorepo-like structure with clear separation for frontend, backend, Helm charts, and specifications.

```
.
├── backend/              # Backend Node.js/TypeScript application
│   ├── src/
│   │   ├── api/          # API routes
│   │   ├── config/       # Configuration files (e.g., database)
│   │   ├── middleware/   # Express middleware
│   │   ├── models/       # Data models (e.g., User, TodoItem)
│   │   └── services/     # Business logic services
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   └── ...
├── frontend/             # Frontend React/TypeScript application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   ├── Dockerfile
│   ├── package.json
│   └── ...
├── helm-charts/          # Helm charts for deployment
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── templates/      # Kubernetes manifest templates
│       │   ├── _helpers.tpl
│       │   ├── frontend-deployment.yaml
│       │   ├── frontend-service.yaml
│       │   ├── backend-deployment.yaml
│       │   ├── backend-service.yaml
│       │   ├── postgresql-deployment.yaml
│       │   └── postgresql-service.yaml
│       │   └── postgresql-pvc.yaml
│       ├── charts/         # Subcharts (e.g., PostgreSQL)
│       └── README.md       # Helm chart specific documentation
├── specs/                # Specification and planning artifacts
│   └── 002-local-k8s-deploy/ # Specific feature/phase specs
│       ├── checklists/
│       │   └── requirements.md
│       ├── contracts/      # API contracts (e.g., OpenAPI)
│       │   └── api.yaml
│       ├── plan.md         # Implementation plan
│       ├── research.md     # Technical decisions and research findings
│       ├── spec.md         # Feature specification
│       ├── tasks.md        # Actionable tasks breakdown
│       └── quickstart.md   # Quickstart deployment guide
├── .dockerignore
├── .eslintignore
├── .eslintrc.json
├── .helmignore
├── .npmignore
├── .prettierignore
├── GEMINI.md
├── .gemini/
├── .specify/
├── history/
└── README.md             # This file
├── backend/.env          # Environment variables for backend (DO NOT COMMIT)
├── frontend/.env         # Environment variables for frontend (DO NOT COMMIT)
├── backend/package.json
├── frontend/package.json
└── ...
## Getting Started

### Prerequisites

Ensure you have the following tools installed and configured:

*   **Docker Desktop**: For containerization.
*   **Minikube**: For local Kubernetes.
*   **Helm**: For Kubernetes package management.
*   **kubectl**: Kubernetes command-line tool.

### Cloning the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Local Deployment Workflow

The deployment process is designed for AI agent execution. Follow these conceptual steps, understanding that AI agents will generate and execute the precise commands.

1.  **Start Minikube Cluster**:
    *   **AI Agent**: `kubectl-ai`
    *   **Action**: Ensure Minikube is running and `kubectl` is configured.
    *   **Conceptual Command**: `kubectl-ai minikube start`

2.  **Containerize Applications**:
    *   **AI Agent**: `Docker AI Agent (Gordon)` / `Claude Code`
    *   **Action**: Build Docker images for frontend and backend.
    *   **Conceptual Commands**: `gordon build --optimize -t todo-frontend:latest ./frontend` and `gordon build --optimize -t todo-backend:latest ./backend`. Fallback available via Claude Code.

3.  **Generate and Deploy Helm Charts**:
    *   **AI Agent**: `AI Agent` / `kubectl-ai`
    *   **Action**: Generate Helm charts and deploy the application.
    *   **Conceptual Command**: `kubectl-ai helm install todo-app helm-charts/todo-app`

4.  **Verify Deployment Health**:
    *   **AI Agent**: `kubectl-ai` / `kagent`
    *   **Action**: Check frontend, backend, and PostgreSQL pod status.
    *   **Conceptual Commands**: `kubectl-ai get pods -l app.kubernetes.io/component=<component-name>`

5.  **Access the Application**:
    *   **AI Agent**: `kubectl-ai`
    *   **Action**: Provide access to the frontend.
    *   **Conceptual Command**: `kubectl-ai minikube service todo-app-frontend`

6.  **AI-Assisted Cluster Management**:
    *   **AI Agents**: `kubectl-ai`, `kagent`
    *   **Actions**: Scaling, debugging, monitoring, and resource optimization.
    *   **Conceptual Commands**: Refer to `helm-charts/todo-app/README.md` for agent-specific commands.

## AI Agent Roles

*   **Docker AI Agent (Gordon)**: Responsible for building and optimizing Docker images.
*   **Claude Code**: Generates Docker commands as a fallback for Gordon.
*   **`kubectl-ai`**: Manages Kubernetes deployments, scaling, debugging, and provides access to services.
*   **`kagent`**: Monitors cluster health, resource utilization, and provides optimization suggestions, also acts as a fallback for `kubectl-ai` failures.

## Contributing

Contributions are welcome following the Spec-Driven Development principles outlined in the project constitution and the defined AI agent workflows.

## License

[Specify License Here]
