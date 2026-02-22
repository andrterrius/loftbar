from uuid import UUID
from typing import Protocol, Optional, Sequence, Any
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.db.models import DBBowl


class IBowlsRepository(Protocol):

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

    async def get_by_name(self, name: str) -> Optional[Any]:
        ...

    async def get_by_category(self, category: str, only_available: bool = False) -> Sequence[Any]:
        ...

    async def get_available(self) -> Sequence[Any]:
        ...

    async def get_bowls_by_filters(
            self,
            category: Optional[str] = None,
            only_available: bool = False,
            order_by: Any = None
    ) -> Sequence[Any]:
        ...

    async def update_availability(self, bowl_id: UUID, is_available: bool) -> Optional[Any]:
        ...

    async def get_unique_categories(self) -> Sequence[str]:
        ...

    async def get_count_by_category(self, category: str, only_available: bool = False) -> int:
        ...


class BowlsRepository(SQLAlchemyRepository[DBBowl], IBowlsRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBBowl)

    async def get_by_name(self, name: str) -> Optional[DBBowl]:
        return await self.get_one(name=name)

    async def get_by_category(self, category: str, only_available: bool = False) -> Sequence[DBBowl]:
        filters = {"category": category}
        if only_available:
            filters["is_available"] = True
        return await self.get_all(**filters)

    async def get_available(self) -> Sequence[DBBowl]:
        return await self.get_all(is_available=True)

    async def get_bowls_by_filters(
            self,
            category: Optional[str] = None,
            only_available: bool = False,
            order_by: Any = None
    ) -> Sequence[DBBowl]:
        filters = {}
        if category:
            filters["category"] = category
        if only_available:
            filters["is_available"] = True
        return await self.get_all(order_by=order_by, **filters)

    async def update_availability(self, bowl_id: UUID, is_available: bool) -> Optional[DBBowl]:
        bowl = await self.get_by_id(bowl_id)
        if bowl:
            bowl.is_available = is_available
            return await self.update(bowl)
        return None

    async def get_unique_categories(self) -> Sequence[str]:
        stmt = select(DBBowl.category).distinct()
        return (await self._session.scalars(stmt)).all()

    async def get_count_by_category(self, category: str, only_available: bool = False) -> int:
        filters = {"category": category}
        if only_available:
            filters["is_available"] = True
        return await self.get_count(**filters)