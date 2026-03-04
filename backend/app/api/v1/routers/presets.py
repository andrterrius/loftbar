from  typing import List
from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.services.abc import BasePresetService
from app.schemas.preset import PresetCreate, PresetUpdate, PresetOut
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