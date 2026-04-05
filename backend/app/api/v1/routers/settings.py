from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BaseSettingsService
from app.schemas.settings import SettingsImagesOut
from app.schemas.auth import CurrentUser


settings_router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    route_class=DishkaRoute
)


@settings_router.get("/images", response_model=SettingsImagesOut)
async def get_settings_images(
    service: FromDishka[BaseSettingsService],
    uow: FromDishka[BaseUnitOfWork],
    current_user: FromDishka[CurrentUser]
):
    """Получить изображения настроек"""
    result = await service.get_images(uow)
    return result
