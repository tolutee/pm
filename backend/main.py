from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import get_database_path, init_db
from routes.board import router as board_router
from routes.chat import router as chat_router
from routes.misc import router as misc_router


def create_app(database_path: Optional[str] = None) -> FastAPI:
    resolved_path = get_database_path(database_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.database_path = resolved_path
        init_db(app)
        yield

    app = FastAPI(title="Project Management MVP", version="0.1.0", lifespan=lifespan)
    app.state.database_path = resolved_path
    app.state.db_conn = None

    app.include_router(misc_router)
    app.include_router(board_router)
    app.include_router(chat_router)

    static_dir = Path(__file__).parent / "static"
    fallback_dir = Path(__file__).parent.parent / "frontend" / "out"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="frontend")
    elif fallback_dir.exists():
        app.mount("/", StaticFiles(directory=str(fallback_dir), html=True), name="frontend")

    return app


app = create_app()
