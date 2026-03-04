from typing import Protocol, List, Optional
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.schemas.order import OrderCreate, OrderOut

from .abc_preset import BasePresetService


class BaseOrderService(Protocol):
    """Протокол сервиса для работы с заказами"""

    async def create_order(self, uow: BaseUnitOfWork, order: OrderCreate, preset_service: BasePresetService,
                           user_id: UUID) -> OrderOut:
        """Получить все пресеты с флагом is_available"""
        ...