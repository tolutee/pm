import os
import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request


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
    app.state.db_conn = conn
