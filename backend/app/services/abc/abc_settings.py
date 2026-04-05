from typing import Protocol, List, Optional

from app.db.uow import BaseUnitOfWork
from app.schemas.preset import PresetBasePrice
from app.schemas.settings import SettingsImagesOut


class BaseSettingsService(Protocol):
    """Протокол сервиса для работы с заказами"""

    async def get_preset_base_price(self, uow: BaseUnitOfWork) -> PresetBasePrice:
        """Получить базовую цену пресета"""
        ...

    async def get_images(self, uow: BaseUnitOfWork) -> SettingsImagesOut:
        """Получить изображения настроек"""
        ...