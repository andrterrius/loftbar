from uuid import UUID
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from app.db.uow import BaseUnitOfWork
from app.db.models import DBUser
from app.services.abc import BaseOrderService, BasePresetService
from app.schemas.order import OrderCreate, OrderOut
from app.schemas.error import ErrorResponse
from app.schemas.auth import CurrentUser

orders_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    route_class=DishkaRoute
)


@orders_router.post(
    "/",
    response_model=OrderOut,
    responses={
        400: {"model": ErrorResponse, "description": "Ошибка валидации. error_type=service_error"},
        401: {"model": ErrorResponse, "description": "Ошибка авторизации. error_type=auth_error"},
    }
)
async def test(
        order: OrderCreate,
        order_service: FromDishka[BaseOrderService],
        preset_service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
        current_user: FromDishka[CurrentUser],
):
    """Создать заказ"""
    return await order_service.create_order(uow, order, preset_service, current_user.id)
