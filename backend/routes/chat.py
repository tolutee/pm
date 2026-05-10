from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status

from auth import require_auth
from board_service import apply_operations_to_board, load_board_for_user, save_board_for_user
from chat_service import chat_with_ai, load_chat_history, save_chat_message
from database import get_db_connection
from models import BoardData, ChatRequest

router = APIRouter(prefix="/api")


@router.post("/chat")
async def chat(
    chat_req: ChatRequest,
    request: Request,
    user: Dict[str, Any] = Depends(require_auth),
) -> Dict[str, Any]:
    conn = get_db_connection(request)
    try:
        history = load_chat_history(conn, user["id"])

        board = load_board_for_user(conn, user["id"])

        ai_response = chat_with_ai(chat_req.message, board, history)

        save_chat_message(conn, user["id"], "user", chat_req.message)
        save_chat_message(conn, user["id"], "assistant", ai_response.message)

        if ai_response.operations:
            apply_operations_to_board(board, ai_response.operations)
            save_board_for_user(conn, user["id"], BoardData(**board))

        board_data = BoardData(**board)

        return {
            "message": ai_response.message,
            "operations": [op.model_dump() for op in ai_response.operations],
            "board": board_data.model_dump(),
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
