from typing import Protocol, List, Optional
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.schemas.order import (
    OrderStatus,
    OrderCreate,
    OrderOutAdmin,
    OrdersHistoryOut
)

from .abc_preset import BasePresetService


class BaseOrderService(Protocol):
    """Протокол сервиса для работы с заказами"""

    async def get_orders_list(
            self,
            uow: BaseUnitOfWork,
            user_id: Optional[UUID] = None,
            user_preset_base_price: float = None
    ) -> List[OrdersHistoryOut]:
        ...

    async def create_order(
            self,
            uow: BaseUnitOfWork,
            order: OrderCreate,
            preset_service: BasePresetService,
            user_id: UUID,
            user_preset_base_price: float = None
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