from pathlib import Path

from starlette.applications import Starlette
from starlette.templating import Jinja2Templates

from .repository.sqlite.sqlite_repository import SqliteRepository
from .routes import create_routes

TEMPLATE_DIRECTORY = Path(__file__).parent / "template"
DB_PATH = str(Path(__file__).parent / "todo.db")
STATIC_FILES_DIRECTORY = str(Path(__file__).parent / "static")


def main():
    template = Jinja2Templates(
        directory=TEMPLATE_DIRECTORY, trim_blocks=True, lstrip_blocks=True
    )
    repository = SqliteRepository.create(DB_PATH)
    routes = create_routes(template, repository, STATIC_FILES_DIRECTORY)
    app = Starlette(debug=True, routes=routes)

    return app
