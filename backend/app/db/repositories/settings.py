from typing import Protocol, Optional, Sequence, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import DBSettings
from .base import SQLAlchemyRepository

class ISettingsRepository(Protocol):
    async def get_by_id(self, _id: int) -> Optional[Any]:
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

    async def delete(self, _id: int) -> None:
        ...

class SettingsRepository(SQLAlchemyRepository[DBSettings]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DBSettings)