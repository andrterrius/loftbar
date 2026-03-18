from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BaseBowlService
from app.schemas.bowl import BowlOut
from app.schemas.auth import CurrentUser


bowls_router = APIRouter(
    prefix="/bowls",
    tags=["bowls"],
    route_class=DishkaRoute
)

@bowls_router.get("", response_model=list[BowlOut])
async def get_available(
    service: FromDishka[BaseBowlService],
    uow: FromDishka[BaseUnitOfWork],
    current_user: FromDishka[CurrentUser]
):
    """Получить список всех доступных чаш"""
    result = await service.get_available(uow)
    return result