from uuid import UUID
from typing import Optional, List
from fastapi import APIRouter, BackgroundTasks
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from sqlalchemy.sql.functions import current_user
from aiogram import Bot
from app.db.uow import BaseUnitOfWork
from app.services.abc import (
    BaseOrderService,
    BasePresetService,
    BaseNotificationService,
)
from app.schemas.order import OrderCreate, OrderOut, OrdersHistoryOut
from app.schemas.error import ErrorResponse
from app.schemas.auth import CurrentUser

orders_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    route_class=DishkaRoute
)


@orders_router.post(
    "",
    response_model=OrderOut,
    responses={
        400: {"model": ErrorResponse, "description": "Ошибка валидации. error_type=service_error"},
        401: {"model": ErrorResponse, "description": "Ошибка авторизации. error_type=auth_error"},
    }
)
async def make_order(
        order: OrderCreate,
        order_service: FromDishka[BaseOrderService],
        preset_service: FromDishka[BasePresetService],
        order_notification_service: FromDishka[BaseNotificationService],
        uow: FromDishka[BaseUnitOfWork],
        tg_bot: FromDishka[Bot],
        current_user: FromDishka[CurrentUser],
        background_tasks: BackgroundTasks,
):
    """Создать заказ"""
    order_out = await order_service.create_order(
        uow,
        order,
        preset_service,
        current_user.id,
        user_preset_base_price=current_user.preset_base_price
    )
    background_tasks.add_task(
        order_notification_service.notify_order_created,
        uow=uow,
        bot=tg_bot,
        order=order_out,
    )

    return OrderOut(
        id=order_out.id,
        daily_number=order_out.daily_number
    )

@orders_router.get("/history",
                    response_model=List[OrdersHistoryOut],
                    responses={
                        401: {"model": ErrorResponse, "description": "Ошибка авторизации. error_type=auth_error"}
                    }
)
async def get_history(
        service: FromDishka[BaseOrderService],
        uow: FromDishka[BaseUnitOfWork],
        current_user: FromDishka[CurrentUser],
):
    """Получить все доступные пресеты"""
    return await service.get_orders_list(
        uow,
        user_id=current_user.id,
        user_preset_base_price=current_user.preset_base_price
    )