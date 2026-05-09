import hashlib
import sqlite3
from typing import Any, Dict

from fastapi import Header, HTTPException, Request, status

from database import get_db_connection


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


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
