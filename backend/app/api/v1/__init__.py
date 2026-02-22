
from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

from .routers.users import users_router
from .routers.flavors import flavors_router


_routers = [
    users_router,
    flavors_router
]

v1_router = APIRouter(
     prefix="/api/v1",
     route_class=DishkaRoute
)

for route in _routers:
    v1_router.include_router(route)