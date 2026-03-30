from typing import Protocol, Any, Dict, Optional, Union
from datetime import datetime
from app.schemas.order import OrderOutAdmin


class BaseNotificationTextService(Protocol):
    """Протокол для сервиса генерации текстов уведомлений о заказах"""

    @staticmethod
    def get_status_emoji(status: Any) -> str:
        """Возвращает эмодзи для статуса заказа."""
        ...

    def generate_order_notification(
            self,
            order: OrderOutAdmin,
            is_update: bool = False
    ) -> str:
        """Генерирует полный текст уведомления о заказе."""
        ...