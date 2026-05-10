from typing import Any, Dict

from fastapi import APIRouter, Depends, Request

from auth import require_auth
from board_service import load_board_for_user, save_board_for_user
from database import get_db_connection
from models import BoardData

router = APIRouter(prefix="/api")


@router.get("/board", response_model=BoardData)
async def get_board(
    request: Request,
    user: Dict[str, Any] = Depends(require_auth),
) -> Dict[str, Any]:
    conn = get_db_connection(request)
    return load_board_for_user(conn, user["id"])


@router.put("/board", response_model=BoardData)
async def update_board(
    board: BoardData,
    request: Request,
    user: Dict[str, Any] = Depends(require_auth),
) -> BoardData:
    conn = get_db_connection(request)
    save_board_for_user(conn, user["id"], board)
    return board


@router.delete("/board")
async def delete_board(
    request: Request,
    user: Dict[str, Any] = Depends(require_auth),
) -> Dict[str, str]:
    conn = get_db_connection(request)
    conn.execute("DELETE FROM kanban_boards WHERE user_id = ?", (user["id"],))
    conn.execute("DELETE FROM chat_history WHERE user_id = ?", (user["id"],))
    conn.commit()
    return {"status": "deleted"}
