from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BaseOrderService, BasePresetService
from app.schemas.order import OrderCreate, OrderOut
from app.schemas.error import ErrorResponse

orders_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    route_class=DishkaRoute
)


@orders_router.post(
    "/",
    response_model=OrderOut,
    responses={
        400: {"model": ErrorResponse, "description": "Ошибка валидации"},
    }
)
async def test(
        order: OrderCreate,
        order_service: FromDishka[BaseOrderService],
        preset_service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Создать заказ"""
    return await order_service.create_order(uow, order, preset_service, "b7fd3e87-1c3a-4d96-8415-394d0cb2be8b")
