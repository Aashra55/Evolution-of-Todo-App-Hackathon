# Quickstart Guide: Local Kubernetes Deployment

**Branch**: `002-local-k8s-deploy` | **Date**: 2026-02-09 | **Plan**: specs/002-local-k8s-deploy/plan.md

This guide provides steps to quickly get the Todo Chatbot application deployed and running on a local Minikube Kubernetes cluster. All operations are designed to be executed by AI agents as defined in the tasks.

## Prerequisites

Ensure the following tools are installed and configured on your system:

1.  **Docker Desktop**: For building and managing container images.
2.  **Minikube**: For running a local Kubernetes cluster.
    *   Refer to the [Minikube documentation](https://minikube.sigs.k8s.io/docs/start/) for installation.
3.  **Helm**: For deploying applications on Kubernetes using Helm charts.
    *   Refer to the [Helm documentation](https://helm.sh/docs/intro/install/) for installation.
4.  **kubectl**: Kubernetes command-line tool (usually installed with Minikube).

## Setup and Deployment Workflow

The entire deployment process is driven by AI agents. The following steps outline the conceptual flow and AI agent actions.

### Step 1: Start and Configure Minikube Cluster

**AI Agent**: `kubectl-ai`
**Action**: Start the Minikube cluster and configure `kubectl` context.
**Tasks**:
*   T035: Implement `kubectl-ai` command to start Minikube cluster.
    *   **Conceptual Command**: `kubectl-ai minikube start`
    *   **Actual Minikube Command**: `minikube start`
*   T036: Implement `kubectl-ai` command to configure `kubectl` context to Minikube.
    *   **Conceptual Command**: `kubectl-ai kubectl config use-context minikube`
    *   **Actual kubectl Command**: `kubectl config use-context minikube`

### Step 2: Containerize Applications

**AI Agent**: `Docker AI Agent (Gordon)` / `Claude Code`
**Action**: Build and optimize Docker images for frontend and backend, with fallback.
**Tasks**:
*   T015-T018: Generate Dockerfiles and define AI agent interactions.
*   T019-T020: Implement fallback logic for Claude Code.
*   T021-T022: Implement Docker image build validation.
**Conceptual Commands**:
*   Frontend: `gordon build --optimize -t todo-frontend:latest ./frontend` or `docker build -t todo-frontend:latest -f frontend/Dockerfile .` (fallback)
*   Backend: `gordon build --optimize -t todo-backend:latest ./backend` or `docker build -t todo-backend:latest -f backend/Dockerfile .` (fallback)

### Step 3: Generate and Deploy Helm Charts

**AI Agent**: `AI Agent` / `kubectl-ai`
**Actions**:
1.  Generate and maintain Helm charts for the application.
    *   **AI Agent Action**: Generate Helm chart structure, templates, and `values.yaml`.
2.  Validate Helm charts (linting and dry-run).
    *   **AI Agent Action**: Perform Helm lint validation.
    *   **AI Agent Action**: Perform Helm template dry-run validation.
3.  Deploy the `todo-app` Helm chart to Minikube.
    *   **Conceptual Command**: `kubectl-ai helm install todo-app helm-charts/todo-app`
    *   **Actual Helm Command**: `helm install todo-app ./helm-charts/todo-app`
**Tasks**: T023-T034

### Step 4: Verify Deployment Health

**AI Agent**: `kubectl-ai`
**Actions**: Verify readiness and health of frontend, backend, and PostgreSQL pods.
**Tasks**: T038, T039, T040
**Conceptual Commands**:
*   Frontend: `kubectl-ai get pods -l app.kubernetes.io/component=frontend --field-selector=status.phase=Running -o json`
*   Backend: `kubectl-ai get pods -l app.kubernetes.io/component=backend --field-selector=status.phase=Running -o json`
*   PostgreSQL: `kubectl-ai get pods -l app.kubernetes.io/component=postgresql --field-selector=status.phase=Running -o json`

### Step 5: Access the Application

**AI Agent**: `kubectl-ai`
**Action**: Provide access to the frontend application.
**Tasks**: T041
*   **Conceptual Command**: `kubectl-ai minikube service todo-app-frontend`
*   **Actual Minikube Command**: `minikube service {{ include "todo-app.fullname" . }}-frontend`

### Step 6: AI-Assisted Cluster Management

**AI Agent**: `kubectl-ai` / `kagent`
**Actions**:
1.  Scale frontend and backend deployments based on load metrics.
    *   **Conceptual Command**: `kubectl-ai scale deployment <deployment-name> --replicas=X`
    *   **Actual kubectl Command**: `kubectl scale deployment <deployment-name> --replicas=X`
    **Tasks**: T042, T043
2.  Debug failing frontend and backend pods and suggest fixes.
    *   **Conceptual Command**: `kubectl-ai debug pod <pod-name> --explain`
    *   **Actual kubectl Command**: `kubectl describe pod <pod-name>` or `kubectl logs <pod-name>`
    **Tasks**: T044, T045
3.  Monitor Minikube cluster health and resource utilization (`kagent`).
    *   **Conceptual Action**: `kagent monitor cluster --metrics`
    **Task**: T046
4.  Optimize resource allocation and suggest improvements (`kagent`).
    *   **Conceptual Action**: `kagent optimize resources --recommendations`
    **Task**: T047
5.  Analyze and repair deployments if `kubectl-ai` fails (`kagent` fallback).
    *   **Conceptual Action**: `kagent analyze-and-repair-deployment <deployment-name> --failure-context <failure-details>`
    **Task**: T048