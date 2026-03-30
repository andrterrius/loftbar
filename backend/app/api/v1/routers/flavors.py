from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BaseFlavorService
from app.schemas.flavor import FlavorCreate, FlavorUpdate, FlavorOut
from app.schemas.auth import CurrentUser


flavors_router = APIRouter(
    prefix="/flavors",
    tags=["flavors"],
    route_class=DishkaRoute
)

@flavors_router.get("", response_model=list[FlavorOut])
async def get_available(
    service: FromDishka[BaseFlavorService],
    uow: FromDishka[BaseUnitOfWork],
    current_user: FromDishka[CurrentUser]
):
    """Получить список всех доступных вкусов"""
    result = await service.get_available(uow)
    return result