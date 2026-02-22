from uuid import UUID
from typing import Protocol, Optional, Sequence, Any
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.db.models import DBLiquid


class ILiquidsRepository(Protocol):

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

    async def get_liquids_by_filters(
            self,
            category: Optional[str] = None,
            only_available: bool = False,
            order_by: Any = None
    ) -> Sequence[Any]:
        ...

    async def update_availability(self, liquid_id: UUID, is_available: bool) -> Optional[Any]:
        ...

    async def get_unique_categories(self) -> Sequence[str]:
        ...

    async def get_count_by_category(self, category: str, only_available: bool = False) -> int:
        ...

    async def get_by_color(self, hex_color: str) -> Sequence[Any]:
        ...

    async def get_with_image(self) -> Sequence[Any]:
        ...


class LiquidsRepository(SQLAlchemyRepository[DBLiquid], ILiquidsRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBLiquid)

    async def get_by_name(self, name: str) -> Optional[DBLiquid]:
        return await self.get_one(name=name)

    async def get_by_category(self, category: str, only_available: bool = False) -> Sequence[DBLiquid]:
        filters = {"category": category}
        if only_available:
            filters["is_available"] = True
        return await self.get_all(**filters)

    async def get_available(self) -> Sequence[DBLiquid]:
        return await self.get_all(is_available=True)

    async def get_liquids_by_filters(
            self,
            category: Optional[str] = None,
            only_available: bool = False,
            order_by: Any = None
    ) -> Sequence[DBLiquid]:
        filters = {}
        if category:
            filters["category"] = category
        if only_available:
            filters["is_available"] = True
        return await self.get_all(order_by=order_by, **filters)

    async def update_availability(self, liquid_id: UUID, is_available: bool) -> Optional[DBLiquid]:
        liquid = await self.get_by_id(liquid_id)
        if liquid:
            liquid.is_available = is_available
            return await self.update(liquid)
        return None

    async def get_unique_categories(self) -> Sequence[str]:
        stmt = select(DBLiquid.category).distinct()
        return (await self._session.scalars(stmt)).all()

    async def get_count_by_category(self, category: str, only_available: bool = False) -> int:
        filters = {"category": category}
        if only_available:
            filters["is_available"] = True
        return await self.get_count(**filters)

    async def get_by_color(self, hex_color: str) -> Sequence[DBLiquid]:
        return await self.get_all(hex_color=hex_color)

    async def get_with_image(self) -> Sequence[DBLiquid]:
        stmt = select(DBLiquid).where(DBLiquid.image_url.isnot(None))
        return (await self._session.scalars(stmt)).all()