from app.db.uow import BaseUnitOfWork
from app.schemas.preset import PresetBasePrice
from app.schemas.settings import SettingsImagesOut

from app.services.abc import BaseSettingsService
from app.core.common import its_evening_now


class SettingsService(BaseSettingsService):
    async def get_preset_base_price(
            self,
            uow: BaseUnitOfWork,
            user_preset_base_price: float = None
    ) -> PresetBasePrice:
        async with uow:
            settings = await uow.settings.get_by_id(1)

            is_evening_price = its_evening_now()
            if is_evening_price:
                if user_preset_base_price:
                    base_price = user_preset_base_price
                else:
                    base_price = settings.preset_base_price_evening
            else:
                base_price = settings.preset_base_price


            return PresetBasePrice(
                base_price=base_price,
                strength_added_price=settings.strength_added_price
            )

    async def get_images(self, uow: BaseUnitOfWork) -> SettingsImagesOut:
        async with uow:
            settings = await uow.settings.get_by_id(1)
            return SettingsImagesOut.model_validate(settings)