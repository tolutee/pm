# Database Design for Project Management MVP

## Goals
- Store Kanban board state persistently in SQLite
- Support multiple users with one board per user
- Keep the MVP design simple by storing the board as JSON
- Allow future expansion to normalized models if needed

## Schema Overview
The database uses SQLite and stores the full Kanban board state as JSON in a single column.
This is the simplest approach for the MVP because the frontend already works with a complete `BoardData` object.

### Tables

#### `users`
Stores user accounts for future support.

- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `username` TEXT NOT NULL UNIQUE
- `password_hash` TEXT
- `created_at` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
- `updated_at` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

For the MVP, authentication is hardcoded in the frontend, but the schema supports real user accounts later.

#### `kanban_boards`
Stores the user-specific Kanban board as JSON.

- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id` INTEGER NOT NULL REFERENCES users(id)
- `board_json` TEXT NOT NULL
- `created_at` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
- `updated_at` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

Constraints:
- Unique constraint on `user_id` to enforce one board per user
- `board_json` contains the full board state for easy persistence and retrieval

## Why JSON?
- The frontend already uses a JSON-friendly board model with columns and cards
- JSON storage keeps the backend simple for MVP
- SQLite supports JSON functions if we need lightweight queries later
- Future versions can migrate to normalized tables if needed

## Example `board_json`
```json
{
  "columns": [
    { "id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"] },
    { "id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"] },
    { "id": "col-progress", "title": "In Progress", "cardIds": ["card-4", "card-5"] },
    { "id": "col-review", "title": "Review", "cardIds": ["card-6"] },
    { "id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"] }
  ],
  "cards": {
    "card-1": { "id": "card-1", "title": "Align roadmap themes", "details": "Draft quarterly themes with impact statements and metrics." },
    "card-2": { "id": "card-2", "title": "Gather customer signals", "details": "Review support tags, sales notes, and churn feedback." },
    "card-3": { "id": "card-3", "title": "Prototype analytics view", "details": "Sketch initial dashboard layout and key drill-downs." }
  }
}
```

## Storage Location
- The SQLite database file will be created if it does not exist
- Recommended location: `backend/pm.db` or `backend/data.db`

## Next Step
- Implement schema creation in backend startup
- Add API endpoints to read and save `kanban_boards.board_json` for the current user
- Use the schema to persist the board across app restarts
