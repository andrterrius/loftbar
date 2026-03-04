
from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

from .routers.users import users_router
from .routers.flavors import flavors_router
from .routers.presets import presets_router
from .routers.liquids import liquids_router
from .routers.bowls import bowls_router
from .routers.order import orders_router

_routers = [
    users_router,
    flavors_router,
    presets_router,
    liquids_router,
    bowls_router,
    orders_router
]

v1_router = APIRouter(
     prefix="/api/v1",
     route_class=DishkaRoute
)

for route in _routers:
    v1_router.include_router(route)