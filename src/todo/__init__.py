from pathlib import Path

from starlette.applications import Starlette
from starlette.config import Config
from starlette.templating import Jinja2Templates

from .repository.sqlite.sqlite_repository import SqliteRepository
from .routes import create_routes

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", cast=str)
TEMPLATE_DIRECTORY = str(Path(__file__).parent / "template")
STATIC_FILES_DIRECTORY = str(Path(__file__).parent / "static")
print(DATABASE_URL)


def main():
    template = Jinja2Templates(
        directory=TEMPLATE_DIRECTORY, trim_blocks=True, lstrip_blocks=True
    )
    repository = SqliteRepository.create(DATABASE_URL)
    routes = create_routes(template, repository, STATIC_FILES_DIRECTORY)
    app = Starlette(debug=DEBUG, routes=routes)

    return app
