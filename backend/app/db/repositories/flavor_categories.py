from uuid import UUID
from typing import List, Protocol, Optional, Sequence, Any
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.db.models import DBFlavorCategory, DBFlavor, DBFlavorCategoryAssociation


class IFlavorCategoriesRepository(Protocol):
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

    async def get_all_sorted(self) -> List[DBFlavorCategory]:
        ...

    async def get_by_ids(self, ids: List[UUID]) -> List[DBFlavorCategory]:
        ...

    async def get_by_name(self, name: str) -> Optional[DBFlavorCategory]:
        ...


class FlavorCategoriesRepository(SQLAlchemyRepository[DBFlavorCategory], IFlavorCategoriesRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBFlavorCategory)

    async def get_all_sorted(self) -> List[DBFlavorCategory]:
        query = (
            select(DBFlavorCategory)
            .where(
                exists().where(
                    DBFlavorCategoryAssociation.category_id == DBFlavorCategory.id,
                    DBFlavorCategoryAssociation.flavor_id == DBFlavor.id,
                    DBFlavor.is_available == True
                )
            )
            .order_by(DBFlavorCategory.order.asc().nulls_last())
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_ids(self, ids: List[UUID]) -> List[DBFlavorCategory]:
        query = select(self.model).where(self.model.id.in_(ids))
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Optional[DBFlavorCategory]:
        return await self.get_one(name=name)