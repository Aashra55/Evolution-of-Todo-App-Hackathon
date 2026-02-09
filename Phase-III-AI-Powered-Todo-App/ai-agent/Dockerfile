# Use a Python base image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app/ai-agent

# Copy pyproject.toml and poetry.lock for dependency installation
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install poetry
RUN poetry install --no-root --no-dev # Install production dependencies

# Copy the rest of your application code
COPY . .

# This AI Agent doesn't expose a direct port for external access in this phase,
# but it runs locally and communicates with the backend MCP server.
# No EXPOSE needed for a standalone agent if not directly served.

# Placeholder command - actual command depends on how the agent is run
CMD ["poetry", "run", "python", "ai-agent/src/agents/main_agent.py"]
