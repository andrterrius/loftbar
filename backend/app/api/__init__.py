from fastapi import FastAPI
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .v1 import v1_router

from .v1.handlers import base_service_exception_handler
from app.exceptions import BaseServiceException

_v_routers = [v1_router]


def include_routers(app: FastAPI) -> None:
    for route in _v_routers:
        app.include_router(route)

def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BaseServiceException, base_service_exception_handler)