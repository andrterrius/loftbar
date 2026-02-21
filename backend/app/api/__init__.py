from fastapi import FastAPI

from .v1 import v1_router

_v_routers = [v1_router]


def include_routers(app: FastAPI) -> None:
    for route in _v_routers:
        app.include_router(route)