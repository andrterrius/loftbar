from uuid import UUID
from typing import List, Protocol, Optional, Sequence, Any
from sqlalchemy import select, desc, asc, nulls_last
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.db.models import DBFlavor


class IFlavorsRepository(Protocol):
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

    async def get_by_ids(self, ids: List[UUID]) -> List[DBFlavor]:
        ...

    async def get_by_name(self, name: str, brand: Optional[str] = None) -> Optional[Any]:
        ...

    async def get_by_brand(self, brand: str, only_available: bool = False) -> Sequence[Any]:
        ...

    async def get_by_category(self, category: str, only_available: bool = False) -> Sequence[Any]:
        ...

    async def get_available(self) -> Sequence[Any]:
        ...

    async def get_flavors_by_filters(
            self,
            brand: Optional[str] = None,
            category: Optional[str] = None,
            only_available: bool = False,
            order_by: Any = None
    ) -> Sequence[Any]:
        ...

    async def update_availability(self, flavor_id: UUID, is_available: bool) -> Optional[Any]:
        ...

    async def get_unique_brands(self) -> Sequence[str]:
        ...

    async def get_unique_categories(self) -> Sequence[str]:
        ...

    async def get_count_by_brand(self, brand: str, only_available: bool = False) -> int:
        ...

    async def get_count_by_category(self, category: str, only_available: bool = False) -> int:
        ...

class FlavorsRepository(SQLAlchemyRepository[DBFlavor], IFlavorsRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBFlavor)

    async def get_by_ids(self, ids: List[UUID]) -> List[DBFlavor]:
        query = select(self.model).where(self.model.id.in_(ids))

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_name(self, name: str, brand: Optional[str] = None) -> Optional[DBFlavor]:
        filters = {"name": name}
        if brand:
            filters["brand"] = brand
        return await self.get_one(**filters)

    async def get_by_brand(self, brand: str, only_available: bool = False) -> Sequence[DBFlavor]:
        filters = {"brand": brand}
        if only_available:
            filters["is_available"] = True
        return await self.get_all(**filters)

    async def get_by_category(self, category: str, only_available: bool = False) -> Sequence[DBFlavor]:
        filters = {"category": category}
        if only_available:
            filters["is_available"] = True
        return await self.get_all(**filters)

    async def get_available(self) -> Sequence[DBFlavor]:
        query = (
            select(self.model)
            .where(self.model.is_available == True)
            .order_by(
                nulls_last(asc(self.model.priority)),
                asc(self.model.name)
            )
        )

        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_flavors_by_filters(
            self,
            brand: Optional[str] = None,
            category: Optional[str] = None,
            only_available: bool = False,
            order_by: Any = None
    ) -> Sequence[DBFlavor]:
        filters = {}

        if brand:
            filters["brand"] = brand
        if category:
            filters["category"] = category
        if only_available:
            filters["is_available"] = True

        return await self.get_all(order_by=order_by, **filters)

    async def update_availability(self, flavor_id: UUID, is_available: bool) -> Optional[DBFlavor]:
        flavor = await self.get_by_id(flavor_id)
        if flavor:
            flavor.is_available = is_available
            return await self.update(flavor)
        return None

    async def get_unique_brands(self) -> Sequence[str]:
        stmt = select(DBFlavor.brand).distinct()
        return (await self._session.scalars(stmt)).all()

    async def get_unique_categories(self) -> Sequence[str]:
        stmt = select(DBFlavor.category).distinct()
        return (await self._session.scalars(stmt)).all()

    async def get_count_by_brand(self, brand: str, only_available: bool = False) -> int:
        filters = {"brand": brand}
        if only_available:
            filters["is_available"] = True
        return await self.get_count(**filters)

    async def get_count_by_category(self, category: str, only_available: bool = False) -> int:
        filters = {"category": category}
        if only_available:
            filters["is_available"] = True
        return await self.get_count(**filters)