from typing import Protocol, Optional, Sequence, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import DBOrder
from app.schemas.order import OrderStatus
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

class OrdersRepository(SQLAlchemyRepository[DBOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DBOrder)

    async def get_by_user_id(self, user_id: UUID) -> Sequence[DBOrder]:
        return await self.get_all(user_id=user_id)