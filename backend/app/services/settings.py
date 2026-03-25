from app.db.uow import BaseUnitOfWork
from app.schemas.preset import PresetBasePrice

from app.services.abc import BaseSettingsService


class SettingsService(BaseSettingsService):
    async def get_preset_base_price(self, uow: BaseUnitOfWork) -> PresetBasePrice:
        async with uow:
            settings = await uow.settings.get_by_id(1)
            return PresetBasePrice(
                base_price=settings.preset_base_price,
                strength_added_price=settings.strength_added_price
            )