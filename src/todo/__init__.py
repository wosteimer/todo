from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.config import Config

from .repository.sqlite_todo_repository import SqlitePool, SqliteTodoRepository
from .routes import create_routes

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", cast=str)
STATIC_FILES_DIRECTORY = str(Path(__file__).parent / "static")


@asynccontextmanager
async def lifespan(_: Starlette):
    pool = SqlitePool()
    await pool.connect(DATABASE_URL)
    yield {"todos": SqliteTodoRepository(pool)}
    await pool.close()


def main():
    routes = create_routes(STATIC_FILES_DIRECTORY)
    app = Starlette(debug=DEBUG, routes=routes, lifespan=lifespan)

    return app
