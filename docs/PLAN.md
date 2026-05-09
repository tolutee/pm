# Detailed Project Plan for Project Management MVP

## Current Status (May 9, 2026)
- **Parts 1-8: COMPLETED** ✅
- **Part 9: AI Chat Backend - NEXT** ⏳
- **Part 10: AI Chat UI - PENDING** ⏳

The MVP core functionality is working: users can sign in, view and interact with a persistent Kanban board. Ready to add AI chat features.

## Part 1: Planning and Documentation
**Goal:** Create comprehensive project documentation and get user approval.

### Substeps:
- [x] Review existing AGENTS.md and PLAN.md
- [x] Analyze existing frontend code structure
- [x] Create frontend/AGENTS.md describing existing code
- [x] Enrich PLAN.md with detailed substeps, checklists, tests, and success criteria
- [x] Get user approval on enriched plan

### Tests:
- N/A (documentation phase)

### Success Criteria:
- [x] frontend/AGENTS.md exists and accurately describes the codebase
- [x] PLAN.md contains detailed implementation steps for all parts
- [x] User has reviewed and approved the plan

## Part 2: Docker and Backend Scaffolding
**Goal:** Set up Docker container with FastAPI backend serving static HTML.

### Substeps:
- [x] Create Dockerfile for Python/FastAPI app
- [x] Create requirements.txt or pyproject.toml with FastAPI, uvicorn, and dependencies
- [x] Create backend/ directory structure
- [x] Implement basic FastAPI app with root endpoint serving "Hello World" HTML
- [x] Add API endpoint that returns JSON response
- [x] Create scripts/start.sh, scripts/stop.sh for Mac/Linux and scripts/start.bat, scripts/stop.bat for Windows
- [x] Test Docker build and run locally
- [x] Verify static HTML serves at / and API endpoint works

### Tests:
- [x] Unit test for FastAPI endpoints
- [x] Integration test for Docker container startup
- [x] Manual test: curl localhost:8000 returns HTML
- [x] Manual test: curl localhost:8000/api/test returns JSON

### Success Criteria:
- [x] Docker container builds successfully
- [x] App runs locally on port 8000
- [x] / serves HTML page
- [x] /api/test returns valid JSON
- [x] Start/stop scripts work on user's OS

## Part 3: Static Frontend Integration
**Goal:** Build and serve the existing Next.js frontend statically.

### Substeps:
- [x] Configure Next.js for static export (output: 'export')
- [x] Update Dockerfile to copy and serve built frontend files
- [x] Modify FastAPI to serve static files from /static or root
- [x] Test that Kanban board loads at /
- [x] Run existing frontend tests to ensure no regressions

### Tests:
- [x] Existing unit tests pass
- [x] Existing e2e tests pass
- [x] Manual test: Kanban board renders correctly in browser
- [x] Manual test: Drag and drop functionality works

### Success Criteria:
- [x] Frontend builds to static files
- [x] Docker container serves Kanban board at /
- [x] All existing tests pass
- [x] UI is fully functional

## Part 4: User Authentication
**Goal:** Add dummy login/logout functionality.

### Substeps:
- [x] Create login page component
- [x] Add authentication state management
- [x] Implement hardcoded login check ("user"/"password")
- [x] Add logout functionality
- [x] Protect Kanban board behind authentication
- [x] Update routing to redirect to login if not authenticated

### Tests:
- [x] Unit tests for auth state management
- [x] E2E test for login flow
- [x] E2E test for logout flow
- [x] E2E test for protected route access

### Success Criteria:
- [x] / redirects to login if not authenticated
- [x] Login with "user"/"password" shows Kanban board
- [x] Logout redirects to login
- [x] Authentication persists across page refreshes

## Part 5: Database Schema Design
**Goal:** Design and document SQLite database schema for Kanban data.

### Substeps:
- [x] Analyze current frontend data structure
- [x] Design database tables for users, boards, columns, cards
- [x] Create SQL schema file
- [x] Document database approach in docs/DATABASE.md
- [x] Get user approval on schema

### Tests:
- N/A (design phase)

### Success Criteria:
- [x] docs/DATABASE.md exists with schema details
- [x] Schema supports multiple users and boards
- [x] User approves database design

## Part 6: Backend API Implementation
**Goal:** Implement CRUD API for Kanban data with SQLite persistence.

### Substeps:
- [x] Set up SQLite persistence layer
- [x] Create database models from schema
- [x] Implement API endpoints for authenticated board persistence
- [x] Add user authentication to API endpoints
- [x] Database auto-creation on startup
- [x] Write comprehensive backend unit tests

### Tests:
- Unit tests for all API endpoints
- Unit tests for database operations
- Integration tests for full CRUD operations
- Test database creation and seeding

### Success Criteria:
- All API endpoints return correct responses
- Data persists across container restarts
- Authentication required for all endpoints
- Backend tests pass with >90% coverage

## Part 7: Frontend-Backend Integration
**Goal:** Connect frontend to backend API for persistent Kanban.

### Substeps:
- [x] Replace frontend state management with API calls
- [x] Implement data fetching on page load
- [x] Add API calls for card/column operations
- [x] Handle loading states and errors
- [x] Update authentication to pass credentials to backend
- [x] Create unit tests for API client

### Tests:
- Unit tests for API integration functions
- E2E tests for full user workflows
- E2E tests for data persistence
- Performance tests for API calls

### Success Criteria:
- Kanban board loads data from backend
- All operations (add/edit/move/delete) persist
- Authentication works end-to-end
- No data loss on refresh
- All tests pass
## Part 8: OpenAI Integration Setup
**Goal:** Set up OpenAI API connectivity in backend.

### Substeps:
- [x] Add OpenAI Python client to dependencies
- [x] Create OpenAI service module
- [x] Implement simple test API endpoint (e.g., "2+2" math)
- [x] Test OpenAI API key configuration
- [x] Verify API calls work in Docker environment

### Tests:
- [x] Unit test for OpenAI service
- [x] Integration test for API endpoint
- [x] Manual test: API returns correct OpenAI response

### Success Criteria:
- [x] OpenAI API calls work from backend
- [x] Test endpoint returns expected response
- [x] No API key exposure in logs
- [x] All 12 tests passing (8 from test_main.py + 4 from test_openai_service.py)

## Part 9: AI Chat Backend
**Goal:** Implement AI chat with Kanban manipulation via structured outputs.

### Substeps:
- [ ] Design structured output schema for AI responses
- [ ] Create chat API endpoint accepting user messages and board state
- [ ] Implement conversation history storage
- [ ] Add AI prompt engineering for Kanban operations
- [ ] Parse structured outputs and apply board changes
- [ ] Comprehensive testing of AI interactions

### Tests:
- Unit tests for structured output parsing
- Integration tests for chat API
- Tests for various AI command scenarios
- Error handling tests for malformed AI responses

### Success Criteria:
- AI can respond to chat messages
- AI can modify Kanban board via structured outputs
- Conversation history maintained
- All AI operations tested and working

## Part 10: AI Chat UI
**Goal:** Add sidebar chat widget with real-time Kanban updates.

### Substeps:
- [ ] Create chat sidebar component
- [ ] Implement chat message display and input
- [ ] Add real-time board updates from AI responses
- [ ] Style chat UI to match design system
- [ ] Handle chat state and history
- [ ] Final integration testing

### Tests:
- Unit tests for chat components
- E2E tests for chat functionality
- E2E tests for AI-driven board updates
- Accessibility tests for chat UI

### Success Criteria:
- Chat sidebar appears alongside Kanban
- Users can send messages to AI
- AI responses update board in real-time
- Chat history persists
- All functionality works end-to-end