from uuid import UUID
from datetime import datetime
from typing import Optional, Sequence
from app.db.uow import BaseUnitOfWork
from app.schemas.flavor import FlavorCreate, FlavorUpdate, FlavorOut, FlavorCategoryOut
from app.db.models import DBFlavor

from app.services.abc import BaseFlavorService


class FlavorService(BaseFlavorService):
    async def create_flavor(self, uow: BaseUnitOfWork, data: FlavorCreate) -> FlavorOut:
        async with uow:
            flavor_data = data.model_dump(exclude_unset=True, exclude={'categories'})

            new_flavor = DBFlavor(**flavor_data)
            created = await uow.flavors.create(new_flavor)

            if data.categories:
                categories = []
                for category_id in data.categories:
                    category = await uow.flavor_categories.get_by_id(category_id)
                    if category:
                        categories.append(category)

                created.categories = categories

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

            # Разделяем обновление полей и категорий
            update_data = data.model_dump(exclude_unset=True, exclude={'categories'})

            # Обновляем обычные поля
            for field, value in update_data.items():
                setattr(flavor, field, value)
            if data.categories is not None:
                categories = []
                for category_id in data.categories:
                    category = await uow.flavor_categories.get_by_id(category_id)
                    if category:
                        categories.append(category)
                flavor.categories = categories

            updated = await uow.flavors.update(flavor)
            return FlavorOut.model_validate(updated)

    async def delete_flavor(self, uow: BaseUnitOfWork, flavor_id: UUID) -> bool:
        async with uow:
            flavor = await uow.flavors.get_by_id(flavor_id)
            if not flavor:
                return False
            await uow.flavors.delete(flavor_id)
            await uow.commit()
            return True

    async def get_all_categories(self, uow: BaseUnitOfWork, sorted_categories=True) -> Sequence[FlavorCategoryOut]:
        async with uow:
            if sorted_categories:
                categories = await uow.flavor_categories.get_all_sorted()
            else:
                categories = await uow.flavor_categories.get_all()
            return [FlavorCategoryOut.model_validate(c) for c in categories]

    async def get_categories_by_flavor(self, uow: BaseUnitOfWork, flavor_id: UUID) -> Sequence[FlavorCategoryOut]:
        async with uow:
            flavor = await uow.flavors.get_by_id(flavor_id)
            if flavor:
                return [FlavorCategoryOut.model_validate(c) for c in flavor.categories]
            return []