from typing import Protocol, Optional, Sequence
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.schemas.flavor import FlavorCreate, FlavorUpdate, FlavorOut


class BaseFlavorService(Protocol):
    async def create_flavor(self, uow: BaseUnitOfWork, data: FlavorCreate) -> FlavorOut:
        ...

    async def get_all(self, uow: BaseUnitOfWork) -> Sequence[FlavorOut]:
        ...

    async def get_available(self, uow: BaseUnitOfWork) -> Sequence[FlavorOut]:
        ...

    async def get_flavor_by_id(self, uow: BaseUnitOfWork, flavor_id: UUID) -> Optional[FlavorOut]:
        ...

    async def update_flavor(self, uow: BaseUnitOfWork, flavor_id: UUID, data: FlavorUpdate) -> Optional[FlavorOut]:
        ...

    async def delete_flavor(self, uow: BaseUnitOfWork, flavor_id: UUID) -> bool:
        ...