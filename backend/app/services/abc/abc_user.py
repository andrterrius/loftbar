from typing import Protocol

from app.db.uow import BaseUnitOfWork
from app.schemas.user import UserCreate, UserResponse



class BaseUserService(Protocol):
    """Протокол сервиса для работы с пользователями"""

    async def get_or_create_by_telegram_id(
            self,
            uow: BaseUnitOfWork,
            telegram_data: UserCreate
    ) -> UserResponse:
        """
        Получить пользователя по Telegram ID или создать нового
        """
        ...