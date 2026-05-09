import json
import sqlite3
import uuid
from typing import Any, Dict, List

from ai_schema import CardOperation
from models import BoardData


DEFAULT_BOARD_DATA: Dict[str, Any] = {
    "columns": [
        {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"]},
        {"id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"]},
        {"id": "col-progress", "title": "In Progress", "cardIds": ["card-4", "card-5"]},
        {"id": "col-review", "title": "Review", "cardIds": ["card-6"]},
        {"id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"]},
    ],
    "cards": {
        "card-1": {"id": "card-1", "title": "Align roadmap themes", "details": "Draft quarterly themes with impact statements and metrics."},
        "card-2": {"id": "card-2", "title": "Gather customer signals", "details": "Review support tags, sales notes, and churn feedback."},
        "card-3": {"id": "card-3", "title": "Prototype analytics view", "details": "Sketch initial dashboard layout and key drill-downs."},
        "card-4": {"id": "card-4", "title": "Refine status language", "details": "Standardize column labels and tone across the board."},
        "card-5": {"id": "card-5", "title": "Design card layout", "details": "Add hierarchy and spacing for scanning dense lists."},
        "card-6": {"id": "card-6", "title": "QA micro-interactions", "details": "Verify hover, focus, and loading states."},
        "card-7": {"id": "card-7", "title": "Ship marketing page", "details": "Final copy approved and asset pack delivered."},
        "card-8": {"id": "card-8", "title": "Close onboarding sprint", "details": "Document release notes and share internally."},
    },
}


def load_board_for_user(conn: sqlite3.Connection, user_id: int) -> Dict[str, Any]:
    row = conn.execute(
        "SELECT board_json FROM kanban_boards WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    if row and row["board_json"]:
        return json.loads(row["board_json"])
    default_board = json.loads(json.dumps(DEFAULT_BOARD_DATA))
    conn.execute(
        "INSERT INTO kanban_boards (user_id, board_json) VALUES (?, ?)",
        (user_id, json.dumps(default_board)),
    )
    conn.commit()
    return default_board


def save_board_for_user(conn: sqlite3.Connection, user_id: int, board: BoardData) -> None:
    board_json = board.model_dump_json()
    existing = conn.execute(
        "SELECT id FROM kanban_boards WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE kanban_boards SET board_json = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
            (board_json, user_id),
        )
    else:
        conn.execute(
            "INSERT INTO kanban_boards (user_id, board_json) VALUES (?, ?)",
            (user_id, board_json),
        )
    conn.commit()


def apply_operations_to_board(board: Dict[str, Any], operations: List[CardOperation]) -> None:
    for op in operations:
        if op.operation == "create":
            if not op.title or not op.columnId:
                continue
            card_id = f"card-{uuid.uuid4().hex[:8]}"
            board["cards"][card_id] = {"id": card_id, "title": op.title, "details": op.details or ""}
            for col in board["columns"]:
                if col["id"] == op.columnId:
                    col["cardIds"].append(card_id)
                    break

        elif op.operation == "update":
            if op.cardId and op.cardId in board["cards"]:
                if op.title:
                    board["cards"][op.cardId]["title"] = op.title
                if op.details is not None:
                    board["cards"][op.cardId]["details"] = op.details

        elif op.operation == "move":
            if op.cardId and op.columnId:
                for col in board["columns"]:
                    if op.cardId in col["cardIds"]:
                        col["cardIds"].remove(op.cardId)
                        break
                for col in board["columns"]:
                    if col["id"] == op.columnId:
                        col["cardIds"].append(op.cardId)
                        break

        elif op.operation == "delete":
            if op.cardId:
                for col in board["columns"]:
                    if op.cardId in col["cardIds"]:
                        col["cardIds"].remove(op.cardId)
                        break
                board["cards"].pop(op.cardId, None)
