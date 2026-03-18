from typing import Protocol, Optional, Sequence, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import case, update, select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import DBOrder, DBPreset, DBPresetFlavor
from app.schemas.order import OrderStatus
from app.exceptions.order import OrderNotFoundException
from app.core.common import utcnow
from .base import SQLAlchemyRepository

class IOrdersRepository(Protocol):
    async def get_by_id(self, _id: UUID) -> Optional[Any]:
        ...

    async def get_one(self, **filters: Any) -> Optional[Any]:
        ...

    async def get_all(self, order_by: Any = None, **filters: Any) -> Sequence[Any]:
        ...

    async def get_count(self, **filters: Any) -> int:
        ...

    async def create(self, instance: Any) -> Any:
        ...

    async def update(self, instance: Any) -> Any:
        ...

    async def delete(self, _id: UUID) -> None:
        ...

    async def get_by_user_id(self, user_id: UUID) -> Sequence[DBOrder]:
        ...

    async def update_status(self, order_id: UUID, status: OrderStatus) -> DBOrder:
        ...

    async def set_admin_notification_sent(self, order_id: UUID) -> None:
        ...

class OrdersRepository(SQLAlchemyRepository[DBOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DBOrder)

    async def get_by_user_id(self, user_id: UUID) -> Sequence[DBOrder]:
        return await self.get_all(user_id=user_id)

    async def update_status(self, order_id: UUID, status: OrderStatus) -> DBOrder:
        now = utcnow()
        update_values = {"status": status}

        if status == OrderStatus.IN_PROGRESS:
            update_values["confirmed_at"] = now
        elif status == OrderStatus.READY:
            update_values["ready_at"] = now
        elif status == OrderStatus.COMPLETED:
            update_values["completed_at"] = now

        query = (
            update(DBOrder)
            .where(DBOrder.id == order_id)
            .values(**update_values)
        )
        await self._session.execute(query)

        result = await self._session.execute(
            select(DBOrder)
            .where(DBOrder.id == order_id)
            .options(
                selectinload(DBOrder.preset).selectinload(DBPreset.preset_flavors).selectinload(DBPresetFlavor.flavor),
                selectinload(DBOrder.preset).selectinload(DBPreset.liquid),
                selectinload(DBOrder.preset).selectinload(DBPreset.bowl),
                selectinload(DBOrder.user),
                selectinload(DBOrder.table)
            )
        )
        updated_order = result.scalar_one_or_none()

        if not updated_order:
            raise OrderNotFoundException()
        return updated_order

    async def set_admin_notification_sent(self, order_id: UUID) -> None:
        query = (
            update(DBOrder)
            .where(DBOrder.id == order_id)
            .values(admin_notification_sent=True)
        )
        await self._session.execute(query)