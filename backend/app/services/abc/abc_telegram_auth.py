from typing import Optional
from telegram_init_data import InitData

from app.db.uow import BaseUnitOfWork
from app.schemas.auth import SuccessAuth
from app.core.security.abc_jwt_service import BaseJWTService

from typing import Protocol


class BaseTgAuthService(Protocol):
    async def authenticate(
            self,
            uow: BaseUnitOfWork,
            jwt_service: BaseJWTService,
            init_data: InitData
    ) -> Optional[SuccessAuth]:
        ...