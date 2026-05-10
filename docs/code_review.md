# Code Review

Date: 2026-05-09
Project: Project Management MVP (Kanban Board with AI Chat)

## Overview

The project is a Kanban board web app with FastAPI backend, Next.js frontend (static export), SQLite persistence, and OpenAI-powered AI chat. Overall the code is clean, well-structured, and follows good practices for an MVP.

---

## Resolved Issues

The following issues identified during the review have been fixed:

| # | Issue | File | Fix |
|---|-------|------|-----|
| 1 | `.env` tracked by git | `.env` | False alarm — `.env` is properly gitignored and not tracked |
| 2 | Backend tests failing (3 of 7) | `backend/main.py` | `database_path` resolved before lifespan, passed into `init_db` via `app.state` |
| 3 | `async` function with no `await` | `backend/chat_service.py` | Removed misleading `async` from `chat_with_ai()` |
| 4 | User message saved before AI responds | `backend/routes/chat.py` | Both user and assistant messages saved together after successful AI response |
| 5 | Column rename saves on every keystroke | `frontend/src/components/KanbanBoard.tsx` | Added `persistBoardDebounced()` with 400ms delay, used for column rename |
| 6 | Auth test wrong signature | `frontend/src/lib/auth.test.ts` | Changed `setAuthenticated(true)` to `setAuthenticated("user", "password")` |
| 7 | `KanbanBoard.test.tsx` truncated data | `frontend/src/components/KanbanBoard.test.tsx` | Mock data was already complete — false alarm |
| 8 | Missing dependencies | `backend/pyproject.toml` | Added `pydantic>=2.0.0` to runtime deps, `httpx>=0.27.0` to dev deps |
| 9 | Docker Python 3.9 vs 3.12 mismatch | `Dockerfile` | Updated base image from `python:3.9-slim` to `python:3.12-slim` |
| 10 | ChatSidebar re-fetches board | `frontend/src/components/ChatSidebar.tsx`, `backend/routes/chat.py`, `frontend/src/lib/api.ts` | Backend now returns updated `board` in chat response; frontend uses it directly |
| 11 | `pytest-output.txt` committed | `.gitignore` | Added `pytest-output.txt` to gitignore |
| 12 | `.gitignore` typo | `.gitignore` | File already has `.ropeproject` — false alarm |
| 13 | SQLite redundant connections | `backend/database.py` | `init_db()` now stores connection on `app.state.db_conn` for reuse by `get_db_connection()` |

**Test results after fixes:** 19/19 backend tests passing, 12/12 frontend tests passing.

---

## Remaining Issues (Not Fixed)

These are acknowledged but not addressed in this pass (scope or MVP appropriateness):

### Medium

#### 1. No rate limiting on chat endpoint

**File:** `backend/routes/chat.py`

The `/api/chat` endpoint calls OpenAI's API which costs money per token. There's no rate limiting, so a user (or malicious actor) could generate unlimited API calls. For an MVP running locally, this is acceptable but worth noting for production.

### Low

#### 2. Duplicate AGENTS.md files

Four `AGENTS.md` files exist (root, `backend/`, `frontend/`, `scripts/`). Their content largely duplicates `CLAUDE.md`. Consider consolidating.

#### 3. No loading indicator for initial board load in ChatSidebar

**File:** `frontend/src/components/ChatSidebar.tsx`

The sidebar doesn't show a loading state during initial mount — only "Ask me to create, move, or update cards."

#### 4. No debounce on rapid drag events

**File:** `frontend/src/components/KanbanBoard.tsx`

Each drag-end triggers `persistBoard()` immediately. With concurrent drags, last-write-wins could lose data. Low risk for single-user MVP.

---

## Positive Observations

1. **Good separation of concerns** — backend is split into routes, services, models, and database layers
2. **Consistent error handling** — API errors propagate cleanly with `APIError` on the frontend and `HTTPException` on the backend
3. **Type safety** — Pydantic models on backend, TypeScript types on frontend
4. **Test coverage** — solid unit test coverage for both backend (19 tests) and frontend (12 unit + 5 e2e)
5. **Clean UI styling** — consistent use of CSS variables, well-structured Tailwind classes
6. **App factory pattern** — `create_app()` makes testing straightforward with temporary databases
7. **Docker packaging** — single-container deployment is appropriate for an MVP
8. **Drag-and-drop** — well-implemented using `@dnd-kit` with proper collision detection and sortable context
9. **AI integration** — structured output parsing (`AIResponse`/`CardOperation`) is a good pattern for LLM interactions

---

## Summary

| Category | Count |
|----------|-------|
| Fixed | 11 |
| Remaining (wontfix for MVP) | 4 |

All test-impacting issues have been resolved. The codebase is healthy and ready for continued development.
