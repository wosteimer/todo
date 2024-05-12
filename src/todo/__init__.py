from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.config import Config

from .repository.sqlite_todo_repository import SqliteTodoRepository
from .routes import create_routes

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", cast=str)
STATIC_FILES_DIRECTORY = str(Path(__file__).parent / "static")


@asynccontextmanager
async def lifespan(_: Starlette):
    todos = SqliteTodoRepository(DATABASE_URL)
    yield {"todos": todos}


def main():
    routes = create_routes(STATIC_FILES_DIRECTORY)
    app = Starlette(debug=DEBUG, routes=routes, lifespan=lifespan)

    return app
