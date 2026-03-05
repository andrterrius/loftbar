from  typing import List
from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BasePresetService, BaseSettingsService
from app.schemas.preset import PresetOut, PresetBasePrice
from app.schemas.auth import CurrentUser
from app.schemas.error import ErrorResponse


presets_router = APIRouter(
    prefix="/presets",
    tags=["presets"],
    route_class=DishkaRoute
)


@presets_router.get("/",
                    response_model=List[PresetOut],
                    responses={
                        401: {"model": ErrorResponse, "description": "Ошибка авторизации. error_type=auth_error"}
                    }
)
async def get_available(
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
        current_user: FromDishka[CurrentUser]
):
    """Получить все доступные пресеты"""
    return await service.get_available(uow)

@presets_router.get("/price",
                    response_model=PresetBasePrice,
                    responses={
                        401: {"model": ErrorResponse, "description": "Ошибка авторизации. error_type=auth_error"}
                    }
)
async def get_base_price(
        settings_service: FromDishka[BaseSettingsService],
        uow: FromDishka[BaseUnitOfWork],
        current_user: FromDishka[CurrentUser]
):
    """Получить базовую цену пресета"""
    return await settings_service.get_preset_base_price(uow)