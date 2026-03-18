from typing import Protocol
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from app.schemas.order import OrderOutAdmin, OrderStatus
from app.services.abc.abc_notification import BaseNotificationTextService
from app.db.uow import BaseUnitOfWork


class BaseNotificationService(Protocol):
    def __init__(self, text_service: BaseNotificationTextService):
        ...
    async def notify_order_created(
            self,
            uow: BaseUnitOfWork,
            bot: Bot,
            order: OrderOutAdmin,
    ) -> None:
        """Отправляет уведомление о создании заказа."""
        ...

    async def notify_order_edited(
            self,
            bot: Bot,
            chat_id: int,
            message_id: int,
            order: OrderOutAdmin,
    ) -> None:
        """Изменяет сообщение при обновлении заказа."""
        ...

    @staticmethod
    def get_order_keyboard(order_id: str, order_status: OrderStatus) -> InlineKeyboardMarkup:
        """Возвращает базовую клавиатуру aiogram"""
        ...