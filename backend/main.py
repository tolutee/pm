import hashlib
import json
import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, Optional
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from openai_service import simple_math_calculation
from chat_service import chat_with_ai
from ai_schema import AIResponse, CardOperation

DEFAULT_BOARD_DATA: Dict[str, Any] = {
    "columns": [
        {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"]},
        {"id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"]},
        {"id": "col-progress", "title": "In Progress", "cardIds": ["card-4", "card-5"]},
        {"id": "col-review", "title": "Review", "cardIds": ["card-6"]},
        {"id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"]},
    ],
    "cards": {
        "card-1": {
            "id": "card-1",
            "title": "Align roadmap themes",
            "details": "Draft quarterly themes with impact statements and metrics.",
        },
        "card-2": {
            "id": "card-2",
            "title": "Gather customer signals",
            "details": "Review support tags, sales notes, and churn feedback.",
        },
        "card-3": {
            "id": "card-3",
            "title": "Prototype analytics view",
            "details": "Sketch initial dashboard layout and key drill-downs.",
        },
        "card-4": {
            "id": "card-4",
            "title": "Refine status language",
            "details": "Standardize column labels and tone across the board.",
        },
        "card-5": {
            "id": "card-5",
            "title": "Design card layout",
            "details": "Add hierarchy and spacing for scanning dense lists.",
        },
        "card-6": {
            "id": "card-6",
            "title": "QA micro-interactions",
            "details": "Verify hover, focus, and loading states.",
        },
        "card-7": {
            "id": "card-7",
            "title": "Ship marketing page",
            "details": "Final copy approved and asset pack delivered.",
        },
        "card-8": {
            "id": "card-8",
            "title": "Close onboarding sprint",
            "details": "Document release notes and share internally.",
        },
    },
}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class Card(BaseModel):
    id: str
    title: str
    details: str


class Column(BaseModel):
    id: str
    title: str
    cardIds: list[str]


class BoardData(BaseModel):
    columns: list[Column]
    cards: dict[str, Card]


class ChatRequest(BaseModel):
    message: str


def get_database_path(explicit_path: Optional[str] = None) -> Path:
    if explicit_path:
        return Path(explicit_path)
    env_path = os.getenv("PM_DB_PATH")
    return Path(env_path) if env_path else Path(__file__).parent / "pm.db"


def ensure_schema(conn: sqlite3.Connection) -> None:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    ).fetchone()
    if row is None:
        schema_path = Path(__file__).parent / "schema.sql"
        conn.executescript(schema_path.read_text())
        conn.commit()


def get_db_connection(request: Request) -> sqlite3.Connection:
    app = request.app
    if not hasattr(app.state, "database_path"):
        app.state.database_path = get_database_path()
    if not hasattr(app.state, "db_conn") or app.state.db_conn is None:
        database_path = app.state.database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(database_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        ensure_schema(conn)
        app.state.db_conn = conn
    return app.state.db_conn


def init_db(app: FastAPI) -> None:
    database_path = getattr(app.state, "database_path", get_database_path())
    database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(database_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    schema_path = Path(__file__).parent / "schema.sql"
    conn.executescript(schema_path.read_text())
    conn.commit()
    conn.close()


def get_user(conn: sqlite3.Connection, username: str, password: str) -> Dict[str, Any]:
    password_hash = hash_password(password)
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if row:
        if row["password_hash"] != password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        return {"id": row["id"], "username": username}

    cursor = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash),
    )
    conn.commit()
    return {"id": cursor.lastrowid, "username": username}


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


async def require_auth(
    request: Request,
    x_username: str = Header(..., alias="X-Username"),
    x_password: str = Header(..., alias="X-Password"),
) -> Dict[str, Any]:
    if x_username != "user" or x_password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    conn = get_db_connection(request)
    return get_user(conn, x_username, x_password)


def save_chat_message(conn: sqlite3.Connection, user_id: int, role: str, message: str) -> None:
    conn.execute(
        "INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message),
    )
    conn.commit()


def load_chat_history(conn: sqlite3.Connection, user_id: int) -> list[Dict[str, str]]:
    rows = conn.execute(
        "SELECT role, message FROM chat_history WHERE user_id = ? ORDER BY created_at ASC",
        (user_id,),
    ).fetchall()
    return [{"role": row["role"], "content": row["message"]} for row in rows]


def apply_operations_to_board(board: Dict[str, Any], operations: list[CardOperation]) -> None:
    """Apply AI operations to the board state."""
    for op in operations:
        if op.operation == "create":
            if not op.title or not op.columnId:
                continue
            card_id = f"card-{uuid.uuid4().hex[:8]}"
            board["cards"][card_id] = {
                "id": card_id,
                "title": op.title,
                "details": op.details or "",
            }
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
                if op.cardId in board["cards"]:
                    del board["cards"][op.cardId]


def create_app(database_path: Optional[str] = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db(app)
        yield

    app = FastAPI(title="Project Management MVP", version="0.1.0", lifespan=lifespan)
    app.state.database_path = get_database_path(database_path)
    app.state.db_conn = None

    @app.get("/api/test")
    async def test_api() -> Dict[str, str]:
        return {"message": "API is working!", "status": "success"}

    @app.get("/api/test-openai")
    async def test_openai(expression: str = "2+2") -> Dict[str, Any]:
        try:
            result = simple_math_calculation(expression)
            return {"expression": expression, "result": result, "status": "success"}
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"OpenAI API key not configured: {str(e)}",
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"OpenAI API error: {str(e)}",
            )

    @app.get("/__health")
    async def health_check() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/board", response_model=BoardData)
    async def get_board(request: Request, user: Dict[str, Any] = Depends(require_auth)) -> Dict[str, Any]:
        conn = get_db_connection(request)
        return load_board_for_user(conn, user["id"])

    @app.put("/api/board", response_model=BoardData)
    async def update_board(
        board: BoardData,
        request: Request,
        user: Dict[str, Any] = Depends(require_auth),
    ) -> BoardData:
        conn = get_db_connection(request)
        save_board_for_user(conn, user["id"], board)
        return board

    @app.delete("/api/board")
    async def delete_board(request: Request, user: Dict[str, Any] = Depends(require_auth)) -> Dict[str, str]:
        conn = get_db_connection(request)
        conn.execute(
            "DELETE FROM kanban_boards WHERE user_id = ?",
            (user["id"],),
        )
        conn.commit()
        return {"status": "deleted"}

    @app.get("/api/me")
    async def get_me(user: Dict[str, Any] = Depends(require_auth)) -> Dict[str, str]:
        return {"username": user["username"]}

    @app.post("/api/chat")
    async def chat(
        chat_req: ChatRequest,
        request: Request,
        user: Dict[str, Any] = Depends(require_auth),
    ) -> Dict[str, Any]:
        """Handle chat message from user and return AI response with board operations."""
        conn = get_db_connection(request)
        
        try:
            history = load_chat_history(conn, user["id"])
            save_chat_message(conn, user["id"], "user", chat_req.message)

            board = load_board_for_user(conn, user["id"])

            ai_response = await chat_with_ai(chat_req.message, board, history)

            save_chat_message(conn, user["id"], "assistant", ai_response.message)

            if ai_response.operations:
                apply_operations_to_board(board, ai_response.operations)
                save_board_for_user(conn, user["id"], BoardData(**board))

            return {
                "message": ai_response.message,
                "operations": [op.model_dump() for op in ai_response.operations],
                "status": "success",
            }
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid AI response: {str(e)}",
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI error: {str(e)}",
            )

    static_dir = Path(__file__).parent / "static"
    fallback_dir = Path(__file__).parent.parent / "frontend" / "out"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="frontend")
    elif fallback_dir.exists():
        app.mount("/", StaticFiles(directory=str(fallback_dir), html=True), name="frontend")
    return app


app = create_app()
