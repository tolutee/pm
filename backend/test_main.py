from pathlib import Path

from fastapi.testclient import TestClient

from main import create_app


auth_headers = {"X-Username": "user", "X-Password": "password"}


def create_test_client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(str(tmp_path / "test.db")))


def test_api_test_endpoint(tmp_path: Path):
    client = create_test_client(tmp_path)

    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    assert data["message"] == "API is working!"
    assert data["status"] == "success"


def test_board_requires_valid_credentials(tmp_path: Path):
    with create_test_client(tmp_path) as client:
        response = client.get("/api/board", headers={"X-Username": "user", "X-Password": "wrong"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"


def test_board_get_and_update_persists(tmp_path: Path):
    with create_test_client(tmp_path) as client:
        get_response = client.get("/api/board", headers=auth_headers)
        assert get_response.status_code == 200
        board = get_response.json()
        assert "columns" in board and "cards" in board
        assert len(board["columns"]) == 5

        updated_board = {"columns": [{"id": "col-backlog", "title": "Backlog", "cardIds": []}], "cards": {}}
        put_response = client.put("/api/board", json=updated_board, headers=auth_headers)
        assert put_response.status_code == 200
        assert put_response.json() == updated_board

        second_get = client.get("/api/board", headers=auth_headers)
        assert second_get.status_code == 200
        assert second_get.json() == updated_board


def test_delete_board_resets_board(tmp_path: Path):
    with create_test_client(tmp_path) as client:
        client.get("/api/board", headers=auth_headers)

        delete_response = client.delete("/api/board", headers=auth_headers)
        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "deleted"

        reset_response = client.get("/api/board", headers=auth_headers)
        assert reset_response.status_code == 200
        assert reset_response.json()["columns"] != []


def test_database_file_is_created(tmp_path: Path):
    db_path = tmp_path / "test.db"
    with create_test_client(tmp_path) as client:
        response = client.get("/api/test")
        assert response.status_code == 200
    assert db_path.exists()
