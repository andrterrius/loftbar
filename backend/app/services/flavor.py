from uuid import UUID
from typing import Optional, Sequence
from app.db.uow import BaseUnitOfWork
from app.db.repositories.flavors import IFlavorsRepository
from app.schemas.flavor import FlavorCreate, FlavorUpdate, FlavorOut
from app.db.models import DBFlavor

from app.services.abc import BaseFlavorService


class FlavorService(BaseFlavorService):
    async def create_flavor(self, uow: BaseUnitOfWork, data: FlavorCreate) -> FlavorOut:
        async with uow:
            new_flavor = DBFlavor(**data.model_dump())
            created = await uow.flavors.create(new_flavor)
            return FlavorOut.model_validate(created)

    async def get_all(self, uow: BaseUnitOfWork) -> Sequence[FlavorOut]:
        async with uow:
            flavors = await uow.flavors.get_all()
            return [FlavorOut.model_validate(f) for f in flavors]

    async def get_available(self, uow: BaseUnitOfWork) -> Sequence[FlavorOut]:
        async with uow:
            flavors = await uow.flavors.get_available()
            return [FlavorOut.model_validate(f) for f in flavors]

    async def get_flavor_by_id(self, uow: BaseUnitOfWork, flavor_id: UUID) -> Optional[FlavorOut]:
        async with uow:
            flavor = await uow.flavors.get_by_id(flavor_id)
            if flavor:
                return FlavorOut.model_validate(flavor)
            return None

    async def update_flavor(self, uow: BaseUnitOfWork, flavor_id: UUID, data: FlavorUpdate) -> Optional[FlavorOut]:
        async with uow:
            flavor = await uow.flavors.get_by_id(flavor_id)
            if not flavor:
                return None
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(flavor, field, value)
            updated = await uow.flavors.update(flavor)
            return FlavorOut.model_validate(updated)

    async def delete_flavor(self, uow: BaseUnitOfWork, flavor_id: UUID) -> bool:
        async with uow:
            flavor = await uow.flavors.get_by_id(flavor_id)
            if not flavor:
                return False
            await uow.flavors.delete(flavor_id)
            return True