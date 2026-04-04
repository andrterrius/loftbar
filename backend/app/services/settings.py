from app.db.uow import BaseUnitOfWork
from app.schemas.preset import PresetBasePrice
from app.schemas.settings import SettingsImagesOut

from app.services.abc import BaseSettingsService


class SettingsService(BaseSettingsService):
    async def get_preset_base_price(self, uow: BaseUnitOfWork) -> PresetBasePrice:
        async with uow:
            settings = await uow.settings.get_by_id(1)
            return PresetBasePrice.model_validate(settings)

    async def get_images(self, uow: BaseUnitOfWork) -> SettingsImagesOut:
        async with uow:
            settings = await uow.settings.get_by_id(1)
            return SettingsImagesOut.model_validate(settings)