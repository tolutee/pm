import json
import sqlite3
from typing import Any, Dict, List, Optional

from openai_service import get_openai_client
from ai_schema import AIResponse, CardOperation


SYSTEM_PROMPT = """You are a helpful Kanban board assistant. Help users manage their project tasks by:
1. Creating new cards when asked
2. Moving cards between columns
3. Updating card details
4. Deleting completed tasks

When responding, provide a natural conversational response and include specific operations to apply to the board.

Available columns: Backlog, Discovery, In Progress, Review, Done
Column IDs: col-backlog, col-discovery, col-progress, col-review, col-done

Always respond with valid JSON in this format:
{
  "message": "Your response to the user",
  "operations": [
    {
      "operation": "create|update|move|delete",
      "cardId": "card-id (required for update/move/delete)",
      "title": "card title (required for create/update)",
      "details": "card details (optional)",
      "columnId": "column-id (required for create/move)"
    }
  ]
}"""


def parse_ai_response(response_text: str) -> AIResponse:
    try:
        data = json.loads(response_text)
        return AIResponse(
            message=data.get("message", ""),
            operations=[CardOperation(**op) for op in data.get("operations", [])],
        )
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Failed to parse AI response: {str(e)}")


def get_board_context(board: Dict[str, Any]) -> str:
    cards = board.get("cards", {})
    lines = []
    for col in board.get("columns", []):
        card_ids = col.get("cardIds", [])
        header = f'{col["title"]} (id: {col["id"]})'
        if card_ids:
            lines.append(header + ":")
            for cid in card_ids:
                if cid in cards:
                    lines.append(f'  - "{cards[cid]["title"]}" (id: {cid})')
        else:
            lines.append(header + ": empty")
    return "Current board:\n" + "\n".join(lines)


def chat_with_ai(
    user_message: str,
    board: Dict[str, Any],
    history: Optional[List[Dict[str, str]]] = None,
) -> AIResponse:
    try:
        client = get_openai_client()
        board_context = get_board_context(board)
        full_prompt = f"{board_context}\n\nUser request: {user_message}"

        messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": full_prompt})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )

        return parse_ai_response(response.choices[0].message.content)

    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"AI chat error: {str(e)}")


def save_chat_message(conn: sqlite3.Connection, user_id: int, role: str, message: str) -> None:
    conn.execute(
        "INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message),
    )
    conn.commit()


def load_chat_history(conn: sqlite3.Connection, user_id: int) -> List[Dict[str, str]]:
    rows = conn.execute(
        "SELECT role, message FROM chat_history WHERE user_id = ? ORDER BY created_at ASC",
        (user_id,),
    ).fetchall()
    return [{"role": row["role"], "content": row["message"]} for row in rows]
