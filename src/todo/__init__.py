from pathlib import Path

from starlette.applications import Starlette
from starlette.config import Config

from .repository.sqlite.sqlite_repository import SqliteRepository
from .routes import create_routes

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", cast=str)
STATIC_FILES_DIRECTORY = str(Path(__file__).parent / "static")


def main():
    repository = SqliteRepository.create(DATABASE_URL)
    routes = create_routes(repository, STATIC_FILES_DIRECTORY)
    app = Starlette(debug=DEBUG, routes=routes)

    return app
