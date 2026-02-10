# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app/backend

# Copy poetry.lock and pyproject.toml
COPY poetry.lock pyproject.toml ./

# Install poetry and project dependencies
RUN pip install poetry && poetry install --no-root --no-dev

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
