import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path

from fastapi.testclient import TestClient
from main import create_app
from ai_schema import AIResponse, CardOperation
from board_service import apply_operations_to_board

auth_headers = {"X-Username": "user", "X-Password": "password"}


def create_test_client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(str(tmp_path / "test.db")))


@patch("routes.chat.chat_with_ai")
def test_chat_endpoint_success(mock_chat, tmp_path: Path):
    """Test successful chat endpoint."""
    # Mock AI response
    ai_response = AIResponse(
        message="I created a new task for you.",
        operations=[
            CardOperation(
                operation="create",
                title="New task",
                details="Task description",
                columnId="col-backlog"
            )
        ]
    )
    mock_chat.return_value = ai_response
    
    client = create_test_client(tmp_path)
    response = client.post(
        "/api/chat",
        json={"message": "Add a new task"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "I created a new task for you."
    assert len(data["operations"]) == 1
    assert data["operations"][0]["operation"] == "create"


@patch("routes.chat.chat_with_ai")
def test_chat_endpoint_moves_card(mock_chat, tmp_path: Path):
    """Test chat endpoint moving a card."""
    ai_response = AIResponse(
        message="I moved the card to In Progress.",
        operations=[
            CardOperation(
                operation="move",
                cardId="card-1",
                columnId="col-progress"
            )
        ]
    )
    mock_chat.return_value = ai_response
    
    client = create_test_client(tmp_path)
    response = client.post(
        "/api/chat",
        json={"message": "Move card-1 to In Progress"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["operations"][0]["operation"] == "move"


@patch("routes.chat.chat_with_ai")
def test_chat_endpoint_requires_auth(mock_chat, tmp_path: Path):
    """Test that chat endpoint requires authentication."""
    client = create_test_client(tmp_path)
    response = client.post(
        "/api/chat",
        json={"message": "Hello"}
    )
    # FastAPI returns 422 when required headers are absent
    assert response.status_code == 422


@patch("routes.chat.chat_with_ai")
def test_chat_endpoint_handles_invalid_response(mock_chat, tmp_path: Path):
    """Test that chat endpoint handles invalid AI response."""
    mock_chat.side_effect = ValueError("Invalid JSON")
    
    client = create_test_client(tmp_path)
    response = client.post(
        "/api/chat",
        json={"message": "test"},
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert "Invalid AI response" in response.json()["detail"]


def test_apply_operations_create_card():
    """Test creating a card operation."""
    board = {
        "columns": [{"id": "col-backlog", "title": "Backlog", "cardIds": []}],
        "cards": {}
    }
    
    ops = [CardOperation(
        operation="create",
        title="New Card",
        details="Details",
        columnId="col-backlog"
    )]
    
    apply_operations_to_board(board, ops)
    
    assert len(board["cards"]) == 1
    assert len(board["columns"][0]["cardIds"]) == 1
    card_id = board["columns"][0]["cardIds"][0]
    assert board["cards"][card_id]["title"] == "New Card"


def test_apply_operations_move_card():
    """Test moving a card operation."""
    board = {
        "columns": [
            {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1"]},
            {"id": "col-progress", "title": "In Progress", "cardIds": []}
        ],
        "cards": {"card-1": {"id": "card-1", "title": "Task", "details": ""}}
    }
    
    ops = [CardOperation(
        operation="move",
        cardId="card-1",
        columnId="col-progress"
    )]
    
    apply_operations_to_board(board, ops)
    
    assert "card-1" not in board["columns"][0]["cardIds"]
    assert "card-1" in board["columns"][1]["cardIds"]


def test_apply_operations_delete_card():
    """Test deleting a card operation."""
    board = {
        "columns": [
            {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1"]}
        ],
        "cards": {"card-1": {"id": "card-1", "title": "Task", "details": ""}}
    }
    
    ops = [CardOperation(
        operation="delete",
        cardId="card-1"
    )]
    
    apply_operations_to_board(board, ops)
    
    assert "card-1" not in board["cards"]
    assert "card-1" not in board["columns"][0]["cardIds"]
