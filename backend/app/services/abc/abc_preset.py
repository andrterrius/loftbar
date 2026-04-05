from typing import Protocol, List, Optional
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.schemas.preset import PresetCreate, PresetUpdate, PresetOut


class BasePresetService(Protocol):
    """Протокол сервиса для работы с пресетами"""

    async def get_all(
            self,
            uow: BaseUnitOfWork,
            user_preset_base_price: float = None
    ) -> List[PresetOut]:
        """Получить все пресеты с флагом is_available"""
        ...

    async def get_available(
            self,
            uow: BaseUnitOfWork,
            user_preset_base_price: float = None
    ) -> List[PresetOut]:
        """Получить только доступные пресеты (is_available=True)"""
        ...

    async def get_by_id(
            self,
            uow: BaseUnitOfWork,
            preset_id: UUID,
            user_preset_base_price: float = None
    ) -> Optional[PresetOut]:
        """Получить пресет по ID со всеми связями"""
        ...

    async def get_by_id_(
            self,
            uow_inited: BaseUnitOfWork,
            preset_id: UUID,
            user_preset_base_price: float = None
    ) -> Optional[PresetOut]:
        """Получить пресет по ID со всеми связями с уже инициализированным uow"""

    async def create(
            self,
            uow: BaseUnitOfWork,
            data: PresetCreate,
            created_by_id: UUID = None,
            user_preset_base_price: float = None
    ) -> PresetOut:
        """Создать новый пресет"""
        ...

    async def create_(
            self,
            uow_inited: BaseUnitOfWork,
            data: PresetCreate,
            created_by_id: UUID = None,
            user_preset_base_price: float = None
    ) -> PresetOut:
        """Создать новый пресет с уже инициализированным uow"""
        ...

    async def update(
            self,
            uow: BaseUnitOfWork,
            preset_id: UUID,
            data: PresetUpdate,
            user_preset_base_price: float = None
    ) -> Optional[PresetOut]:
        """Обновить существующий пресет"""
        ...

    async def delete(self, uow: BaseUnitOfWork, preset_id: UUID) -> None:
        """Удалить пресет"""
        ...