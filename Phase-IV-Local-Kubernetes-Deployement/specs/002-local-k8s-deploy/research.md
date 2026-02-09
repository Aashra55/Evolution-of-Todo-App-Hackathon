# Research Findings: Local Kubernetes Deployment

**Branch**: `002-local-k8s-deploy` | **Date**: 2026-02-09 | **Plan**: specs/002-local-k8s-deploy/plan.md

## Resolved Clarifications

### 1. Language/Version for Frontend and Backend Applications

-   **Decision**:
    -   **Frontend**: React (JavaScript/TypeScript)
    -   **Backend**: Node.js (JavaScript/TypeScript)
-   **Rationale**: These technologies represent a modern, widely adopted web stack with robust community support, extensive tooling, and excellent compatibility with Docker and Kubernetes containerization. They are suitable for the scale and functionality implied by a "Todo Chatbot" and are common choices for such applications.
-   **Alternatives Considered**:
    -   *Frontend*: Angular, Vue.js (also modern but React is often favored for its flexibility and ecosystem).
    -   *Backend*: Python (FastAPI, Flask, Django), Go (efficient for microservices). While viable, Node.js/TypeScript aligns well with a potential shared language skillset if the frontend is also JavaScript/TypeScript based.

### 2. Backend Storage Solution

-   **Decision**: PostgreSQL relational database.
-   **Rationale**: PostgreSQL is an enterprise-grade, open-source relational database known for its reliability, feature richness, and strong support within Kubernetes ecosystems. It's well-suited for structured data like user tasks, and there are mature Helm charts and operators available for its deployment and management on Kubernetes.
-   **Alternatives Considered**:
    -   *SQLite*: Simple for single-file, local development, but not suitable for a multi-container Kubernetes deployment requiring persistent, shared storage.
    -   *MongoDB*: A NoSQL database. While flexible, a relational model is often a better fit for the structured nature of a Todo application's data.
    -   *In-memory databases*: Not suitable for persistent data storage.

### 3. Testing Frameworks and Methodologies

-   **Decision**:
    -   **Containerization Validation**:
        -   **Docker Build Output Analysis**: Verify successful build, identify warnings.
        -   **Docker Image Scanning**: Use security scanners (e.g., Trivy) for known vulnerabilities.
        -   **Basic Container Runtime Tests**: Verify container starts, exposes correct ports, and basic commands execute within the container.
    -   **Helm Chart Validation**:
        -   **Helm Lint**: Static analysis to check for chart correctness and best practices.
        -   **Helm Template Dry-Run**: Generate Kubernetes manifests without deploying, then validate against Kubernetes API schema and best practices.
    -   **Deployment Validation on Kubernetes**:
        -   **Kubernetes Readiness/Liveness Probes**: Ensure deployed pods are healthy and responsive.
        -   **Service Endpoint Accessibility Checks**: Verify external access to the frontend and backend services.
        -   **Integration Tests**: Automated tests to confirm end-to-end application functionality on the deployed cluster.
-   **Rationale**: This layered approach covers validation at each stage of the deployment pipeline, from image creation to application functionality on Kubernetes, ensuring robustness and security. These methods are standard practices in cloud-native development.
-   **Alternatives Considered**: More extensive end-to-end testing suites (can be integrated in later phases), reliance solely on manual verification (violates AI-driven mandate).
