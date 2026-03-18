import logging
from uuid import UUID
from typing import Optional

from aiogram import types
from aiogram.types import CallbackQuery

from app.models.callback_data import OrderCallback
from app.models.enums import OrderStatus
from app.models.schemas import OrderStatusUpdateTelegram, UserResponse
from app.services.api_client import APIClient

logger = logging.getLogger(__name__)


async def process_order_callback(
        callback: CallbackQuery,
        callback_data: OrderCallback,
        api_user: Optional[UserResponse],
        api_client: Optional[APIClient]
):
    """Обработчик callback'ов от заказов"""
    logger.info(f"Received order callback: {callback_data}")

    if not api_user or not api_user.is_admin:
        return await callback.answer("Вы не админ!", show_alert=True)

    try:
        order_update = OrderStatusUpdateTelegram(
            id=UUID(callback_data.order_id),
            status=OrderStatus(callback_data.action),
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        logger.info(f"Order update: {order_update}")

        success = await api_client.update_order_status(order_update)

        if success:
            await callback.answer("Статус обновлен успешно!")
            # Здесь можно добавить обновление сообщения с заказом
        else:
            await callback.answer(
                "Не удалось обновить статус заказа",
                show_alert=True
            )
    except ValueError as e:
        logger.error(f"Invalid order data: {e}")
        await callback.answer(
            "Некорректные данные заказа",
            show_alert=True
        )


def register_callbacks(dp):
    """Регистрация всех callback'ов"""
    dp.callback_query.register(process_order_callback, OrderCallback.filter())