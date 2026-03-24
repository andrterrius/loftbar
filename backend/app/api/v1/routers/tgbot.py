from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, Response
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from aiogram import Bot

from app.db.uow import BaseUnitOfWork
from app.services.abc import (
    BaseUserService,
    BaseOrderService,
    BaseNotificationService,
    BasePresetService
)

from app.schemas.tgbot import TgBotAuthInfo
from app.schemas.user import UserCreate, UserResponse
from app.schemas.order import OrderStatusUpdateTelegram

#РОУТЕР ДЛЯ СОХРАНЕНИЯ ПОЛЬЗОВАТЕЛЕЙ БОТА И ДЛЯ УПРАВЛЕНИЯ СТАТУСАМИ ЗАКАЗОВ ЧЕРЕЗ ТГ БОТА
tgbot_router = APIRouter(
    prefix="/tgbot",
    tags=["tgbot"],
    route_class=DishkaRoute,
)

@tgbot_router.get("", response_model=UserResponse)
async def get_user(
    tg_user: UserCreate,
    tg_bot_info: FromDishka[TgBotAuthInfo],
    user_service: FromDishka[BaseUserService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Получить юзера"""
    return await user_service.get_or_create_by_telegram_id(uow, tg_user)

@tgbot_router.post("/order/status")
async def update_order_status(
    order_status: OrderStatusUpdateTelegram,
    tg_bot_info: FromDishka[TgBotAuthInfo],
    order_service: FromDishka[BaseOrderService],
    uow: FromDishka[BaseUnitOfWork],
    tg_bot: FromDishka[Bot],
    order_notification_service: FromDishka[BaseNotificationService],
    preset_service: FromDishka[BasePresetService],
    background_tasks: BackgroundTasks,
):
    """Обновить статус заказа"""
    order_out = await order_service.update_order_status(uow, order_status.id, order_status.status, preset_service)

    notify_answer = await order_notification_service.notify_order_edited(
        bot=tg_bot,
        chat_id=order_status.chat_id,
        message_id=order_status.message_id,
        order=order_out,
    )

    return order_out