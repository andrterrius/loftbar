from typing import Protocol, List, Optional
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.schemas.order import OrderStatus, OrderCreate, OrderOutAdmin

from .abc_preset import BasePresetService


class BaseOrderService(Protocol):
    """Протокол сервиса для работы с заказами"""

    async def create_order(
            self,
            uow: BaseUnitOfWork,
            order: OrderCreate,
            preset_service: BasePresetService,
            user_id: UUID
    ) -> OrderOutAdmin:
        """Получить все пресеты с флагом is_available"""
        ...

    async def update_order_status(
            self,
            uow: BaseUnitOfWork,
            order_id: UUID,
            new_status: OrderStatus,
            preset_service: BasePresetService,
            user_id: Optional[UUID] = None
    ) -> OrderOutAdmin:
        """Обновить статус заказа"""
        ...