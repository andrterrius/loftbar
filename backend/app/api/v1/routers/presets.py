from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.services.abc import BasePresetService
from app.schemas.preset import PresetCreate, PresetUpdate, PresetOut

presets_router = APIRouter(
    prefix="/presets",
    tags=["presets"],
    route_class=DishkaRoute
)


@presets_router.get("/", response_model=list[PresetOut])
async def get_available(
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Получить все доступные пресеты"""
    return await service.get_available(uow)