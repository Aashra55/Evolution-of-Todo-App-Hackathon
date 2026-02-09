# Use a Python base image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app/backend

# Copy pyproject.toml and poetry.lock for dependency installation
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install poetry
RUN poetry install --no-root --no-dev # Install production dependencies

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
