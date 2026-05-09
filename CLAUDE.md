# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Kanban board web app with an AI chat sidebar. Users authenticate with hardcoded credentials ("user"/"password"), manage cards across fixed columns (Backlog → Discovery → In Progress → Review → Done), and issue natural-language commands via chat that the backend translates into board operations via OpenAI (gpt-4o).

## Commands

### Backend
Run from the `backend/` directory unless otherwise noted.

```bash
uvicorn main:app --reload          # dev server on :8000
pytest                             # all tests
pytest test_main.py::test_name     # single test
```

### Frontend
Run from the `frontend/` directory.

```bash
npm run dev                        # dev server (Next.js)
npm run build                      # static export to out/
npm run lint                       # ESLint
npm run test                       # Vitest unit tests (watch mode)
npm run test:unit                  # unit tests (run once)
npx vitest run src/lib/auth.test.ts  # single unit test file
npm run test:e2e                   # Playwright E2E tests
npm run test:all                   # unit + E2E
```

### Docker (project root)
```bash
scripts/start.bat    # Windows: build image, start container on :8000
scripts/stop.bat     # Windows: stop + remove container
```

The Docker build copies the Next.js static export into `backend/static/`, which FastAPI serves at `/`.

## Architecture

```
frontend/  → Next.js static export (React 19, Tailwind v4, @dnd-kit)
backend/   → FastAPI + SQLite (uvicorn, openai)
```

**Auth flow**: Frontend stores username/password in localStorage on login. Every API call sends `X-Username` / `X-Password` headers. Backend's `require_auth()` dependency validates against hardcoded values and looks up/creates the user row in SQLite.

**Board persistence**: Board state is stored as a single JSON blob per user in `kanban_boards.board_json`. The frontend fetches on mount and PUTs the full board on any change.

**AI chat flow**: `POST /api/chat` → `chat_service.py` builds a conversation from `chat_history` (SQLite) → calls OpenAI with structured output → parses into `AIResponse` (list of `CardOperation`) → applies operations to board in-memory → persists updated board + chat turns → returns new board state + assistant message.

## Key Files

| File | Role |
|------|------|
| `backend/main.py` | FastAPI app factory, all routes, `require_auth()`, `init_db()` |
| `backend/schema.sql` | SQLite schema: `users`, `kanban_boards`, `chat_history` |
| `backend/chat_service.py` | Builds prompt, calls OpenAI, applies `CardOperation` list to board |
| `backend/openai_service.py` | OpenAI client wrapper |
| `backend/ai_schema.py` | Pydantic models: `AIResponse`, `CardOperation` |
| `frontend/src/components/AuthGate.tsx` | Top-level auth router (localStorage → LoginPage or KanbanBoard) |
| `frontend/src/components/KanbanBoard.tsx` | Main board, fetches/persists data, owns drag-drop state |
| `frontend/src/lib/api.ts` | Typed fetch wrapper with auto-auth headers, custom `APIError` |

## API Routes

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/` | — | Serves static frontend |
| GET | `/__health` | — | Health probe |
| GET | `/api/test` | — | Sanity check |
| GET | `/api/me` | ✓ | Current user info |
| GET | `/api/board` | ✓ | Fetch board JSON |
| PUT | `/api/board` | ✓ | Save board JSON |
| DELETE | `/api/board` | ✓ | Reset board to default |
| POST | `/api/chat` | ✓ | AI chat + board ops |

## Data Models

```typescript
// Frontend (frontend/src/lib/kanban.ts)
type Card   = { id: string; title: string; details: string }
type Column = { id: string; title: string; cardIds: string[] }
type BoardData = { columns: Column[]; cards: Record<string, Card> }
```

```python
# Backend (backend/ai_schema.py)
class CardOperation(BaseModel):
    operation: str        # "create" | "update" | "move" | "delete"
    cardId: Optional[str]
    title: Optional[str]
    details: Optional[str]
    columnId: Optional[str]
```

## Environment

Requires `backend/.env` with:
```
OPENAI_API_KEY=sk-proj-...
```

SQLite database is auto-created at `backend/pm.db` on first startup.

## Implementation Status

See `docs/PLAN.md` for the full 10-part roadmap. Parts 1–8 are complete (Docker, static frontend, auth, DB, board CRUD, OpenAI connectivity). Part 9 (AI chat backend) is in progress. Part 10 (AI chat UI) is next.
