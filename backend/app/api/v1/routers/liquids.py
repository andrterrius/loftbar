from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BaseLiquidService
from app.schemas.liquid import LiquidOut

liquids_router = APIRouter(
    prefix="/liquids",
    tags=["liquids"],
    route_class=DishkaRoute
)

@liquids_router.get("", response_model=list[LiquidOut])
async def get_available(
    service: FromDishka[BaseLiquidService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Получить список всех доступных жидкостей"""
    result = await service.get_available(uow)
    return result