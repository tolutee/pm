# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy pyproject.toml from backend
COPY backend/pyproject.toml ./

# Install dependencies
RUN uv pip install --system -r pyproject.toml

# Copy backend application code
COPY backend/ .

# Copy built frontend static files
COPY frontend/out ./static

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]