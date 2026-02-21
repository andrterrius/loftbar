
from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

from .routers.test import test_router

_routers = [test_router]

v1_router = APIRouter(
     prefix="/api/v1",
     route_class=DishkaRoute
)

for route in _routers:
    v1_router.include_router(route)