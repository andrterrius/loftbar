from uuid import UUID
from typing import Protocol, Optional, Sequence, Any, List
from sqlalchemy import select, func, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import SQLAlchemyRepository
from app.db.models import DBPreset, DBPresetFlavor, DBFlavor


class IPresetsRepository(Protocol):
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

    async def get_by_category(self, category: str, order_by: Any = None) -> Sequence[Any]:
        ...

    async def get_by_price_range(self, min_price: float, max_price: float) -> Sequence[Any]:
        ...

    async def get_by_liquid(self, liquid_id: UUID) -> Sequence[Any]:
        ...

    async def get_by_bowl(self, bowl_id: UUID) -> Sequence[Any]:
        ...

    async def get_by_created_by(self, user_id: UUID) -> Sequence[Any]:
        ...

    async def get_with_flavors(self, preset_id: UUID) -> Optional[Any]:
        ...

    async def get_with_relations(self, preset_id: UUID) -> Optional[Any]:
        ...

    async def add_flavor_to_preset(self, preset_id: UUID, flavor_id: UUID, percent: float) -> Optional[Any]:
        ...

    async def remove_flavor_from_preset(self, preset_id: UUID, flavor_id: UUID) -> bool:
        ...

    async def update_flavor_percent(self, preset_id: UUID, flavor_id: UUID, percent: float) -> Optional[Any]:
        ...

    async def get_preset_flavors(self, preset_id: UUID) -> Sequence[Any]:
        ...

    async def get_by_flavors(self, flavor_ids: List[UUID], match_all: bool = False) -> Sequence[Any]:
        ...

    async def get_popular_presets(self, limit: int = 10) -> Sequence[Any]:
        ...

    async def get_unique_categories(self) -> Sequence[str]:
        ...

    async def get_count_by_category(self, category: str) -> int:
        ...

    async def get_count_by_price_range(self, min_price: float, max_price: float) -> int:
        ...


class PresetsRepository(SQLAlchemyRepository[DBPreset], IPresetsRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBPreset)

    async def get_by_name(self, name: str) -> Optional[DBPreset]:
        return await self.get_one(name=name)

    async def get_by_category(self, category: str, order_by: Any = None) -> Sequence[DBPreset]:
        return await self.get_all(order_by=order_by, category=category)

    async def get_by_price_range(self, min_price: float, max_price: float) -> Sequence[DBPreset]:
        stmt = select(DBPreset).where(
            and_(
                DBPreset.price >= min_price,
                DBPreset.price <= max_price
            )
        )
        return (await self._session.scalars(stmt)).all()

    async def get_by_liquid(self, liquid_id: UUID) -> Sequence[DBPreset]:
        return await self.get_all(liquid_id=liquid_id)

    async def get_by_bowl(self, bowl_id: UUID) -> Sequence[DBPreset]:
        return await self.get_all(bowl_id=bowl_id)

    async def get_by_created_by(self, user_id: UUID) -> Sequence[DBPreset]:
        return await self.get_all(created_by_id=user_id)

    async def get_with_flavors(self, preset_id: UUID) -> Optional[DBPreset]:
        stmt = (
            select(DBPreset)
            .where(DBPreset.id == preset_id)
            .options(selectinload(DBPreset.preset_flavors).selectinload(DBPresetFlavor.flavor))
        )
        return await self._session.scalar(stmt)

    async def get_with_relations(self, preset_id: UUID) -> Optional[DBPreset]:
        stmt = (
            select(DBPreset)
            .where(DBPreset.id == preset_id)
            .options(
                selectinload(DBPreset.liquid),
                selectinload(DBPreset.bowl),
                selectinload(DBPreset.created_by),
                selectinload(DBPreset.preset_flavors).selectinload(DBPresetFlavor.flavor)
            )
        )
        return await self._session.scalar(stmt)

    async def add_flavor_to_preset(self, preset_id: UUID, flavor_id: UUID, percent: float) -> Optional[
        DBPresetFlavor]:
        stmt = select(DBPresetFlavor).where(
            and_(
                DBPresetFlavor.preset_id == preset_id,
                DBPresetFlavor.flavor_id == flavor_id
            )
        )
        existing = await self._session.scalar(stmt)

        if existing:
            existing.percent = percent
            await self._session.flush()
            await self._session.refresh(existing)
            return existing
        else:
            preset_flavor = DBPresetFlavor(
                preset_id=preset_id,
                flavor_id=flavor_id,
                percent=percent
            )
            self._session.add(preset_flavor)
            await self._session.flush()
            await self._session.refresh(preset_flavor)
            return preset_flavor

    async def remove_flavor_from_preset(self, preset_id: UUID, flavor_id: UUID) -> bool:
        stmt = delete(DBPresetFlavor).where(
            and_(
                DBPresetFlavor.preset_id == preset_id,
                DBPresetFlavor.flavor_id == flavor_id
            )
        )
        result = await self._session.execute(stmt)
        return result.rowcount > 0

    async def update_flavor_percent(self, preset_id: UUID, flavor_id: UUID, percent: float) -> Optional[
        DBPresetFlavor]:
        stmt = select(DBPresetFlavor).where(
            and_(
                DBPresetFlavor.preset_id == preset_id,
                DBPresetFlavor.flavor_id == flavor_id
            )
        )
        preset_flavor = await self._session.scalar(stmt)

        if preset_flavor:
            preset_flavor.percent = percent
            await self._session.flush()
            await self._session.refresh(preset_flavor)
            return preset_flavor
        return None

    async def get_preset_flavors(self, preset_id: UUID) -> Sequence[DBPresetFlavor]:
        stmt = (
            select(DBPresetFlavor)
            .where(DBPresetFlavor.preset_id == preset_id)
            .options(selectinload(DBPresetFlavor.flavor))
        )
        return (await self._session.scalars(stmt)).all()

    async def get_unique_categories(self) -> Sequence[str]:
        stmt = select(DBPreset.category).distinct()
        return (await self._session.scalars(stmt)).all()

    async def get_count_by_category(self, category: str) -> int:
        return await self.get_count(category=category)

    async def get_count_by_price_range(self, min_price: float, max_price: float) -> int:
        stmt = select(func.count()).select_from(DBPreset).where(
            and_(
                DBPreset.price >= min_price,
                DBPreset.price <= max_price
            )
        )
        return await self._session.scalar(stmt)