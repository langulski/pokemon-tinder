from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.routes.pokemon import router
from src.routes.login import auth_router


api = FastAPI(
    title="Pokemon API",
)

api.mount(
    "/static",
    StaticFiles(
        directory=Path(__file__).parent.parent.absolute() / "templates/static/"
    ),
    name="static",
)
routers = [router, auth_router]


[api.include_router(route) for route in routers]
