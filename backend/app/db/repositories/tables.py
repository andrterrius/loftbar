from uuid import UUID
from typing import Protocol, Optional, Sequence, Any
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.db.models import DBTable


class ITablesRepository(Protocol):
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

    async def get_by_name(self, name: str) -> Optional[DBTable]:
        ...

class TablesRepository(SQLAlchemyRepository[DBTable], ITablesRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBTable)
    async def get_by_name(self, name: str) -> Optional[DBTable]:
        return await self.get_one(name=name)