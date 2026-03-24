from aiogram.types import InlineKeyboardMarkup
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.uow import BaseUnitOfWork
from app.schemas.order import OrderOutAdmin, OrderStatus
from app.services.abc.abc_notification import BaseNotificationTextService
from app.services.abc.abc_order_notification import BaseNotificationService

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from enum import Enum
from typing import Optional

class OrderCallback(CallbackData, prefix="order"):
    action: str
    order_id: str
    status: Optional[str] = None

class TelegramNotificationService(BaseNotificationService):
    def __init__(self, text_service: BaseNotificationTextService):
        self.text_service = text_service

    async def notify_order_created(
            self,
            uow: BaseUnitOfWork,
            bot: Bot,
            order: OrderOutAdmin,
    ) -> None:
        """Уведомление о новом заказе"""
        async with uow:
            text = self.text_service.generate_order_notification(
                order=order,
                is_update=False
            )
            admins = await uow.users.get_admins()
            for admin in admins:
                try:
                    await bot.send_message(
                        chat_id=admin.telegram_id,
                        text=text,
                        reply_markup=self.get_order_keyboard(order_id=str(order.id), order_status=order.status)
                    )
                except:
                    pass

            await uow.orders.set_admin_notification_sent(order.id)

    async def notify_order_edited(
            self,
            bot: Bot,
            chat_id: int,
            message_id: int,
            order: OrderOutAdmin,
    ) -> None:
        """Уведомление о новом заказе"""
        text = self.text_service.generate_order_notification(
            order=order,
            is_update=True
        )
        print(text)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=self.get_order_keyboard(order_id=str(order.id), order_status=order.status)
        )

    @staticmethod
    def get_order_keyboard(order_id: str, order_status: OrderStatus) -> InlineKeyboardMarkup:
        """Кнопки для заказа (принимает строку)"""
        builder = InlineKeyboardBuilder()
        if order_status == OrderStatus.PENDING:
            builder.row(
                InlineKeyboardButton(
                    text="✅ Принять заказ",
                    callback_data=OrderCallback(action="in_progress", order_id=order_id).pack()
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=OrderCallback(action="cancelled", order_id=order_id).pack()
                )
            )

        elif order_status == OrderStatus.IN_PROGRESS:
            builder.row(
                InlineKeyboardButton(
                    text="🍽 Готов к выдаче",
                    callback_data=OrderCallback(action="ready", order_id=order_id).pack()
                )
            )

        elif order_status == OrderStatus.READY:
            builder.row(
                InlineKeyboardButton(
                    text="✅ Выдан клиенту",
                    callback_data=OrderCallback(action="completed", order_id=order_id).pack()
                )
            )

        else:
            builder.row()

        return builder.as_markup()