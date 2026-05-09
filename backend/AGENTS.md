# Backend Code Description

## Overview
The backend is a FastAPI application written in Python that serves the static Next.js frontend and provides REST API endpoints for Kanban board persistence. It uses SQLite for data storage and includes user authentication.

## Key Components

### main.py
- FastAPI application setup with lifespan management
- Static file serving for the Next.js frontend
- SQLite database initialization and schema creation
- API endpoints for board CRUD operations
- User authentication middleware

### schema.sql
- SQLite database schema definition
- Tables: users, kanban_boards
- Supports multiple users and boards for future expansion

### test_main.py
- Comprehensive unit tests for all API endpoints
- Tests authentication, board persistence, and database operations
- Uses pytest and httpx for testing

## API Endpoints
- `GET /`: Serves the static HTML frontend
- `GET /api/board`: Get user's Kanban board (authenticated)
- `PUT /api/board`: Update user's Kanban board (authenticated)
- `DELETE /api/board`: Reset user's Kanban board (authenticated)
- `GET /api/me`: Get current user info (authenticated)

## Authentication
- Uses hardcoded credentials ("user"/"password") for MVP
- Headers: X-Username, X-Password
- Database supports multiple users for future expansion

## Dependencies
- fastapi: Web framework
- uvicorn: ASGI server
- sqlite3: Database
- pydantic: Data validation
- httpx: HTTP client for tests

## Docker Integration
- Runs in Docker container with Python 3.12
- Uses uv for package management
- Serves on port 8000
- Auto-creates database on startup