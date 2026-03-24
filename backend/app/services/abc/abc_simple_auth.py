from typing import Optional

from app.db.uow import BaseUnitOfWork
from app.schemas.auth import LoginSimpleRequest, SuccessAuth
from app.core.security.abc_jwt_service import BaseJWTService

from typing import Protocol


class BaseSimpleAuthService(Protocol):
    async def authenticate(
            self,
            uow: BaseUnitOfWork,
            jwt_service: BaseJWTService,
            login_data: LoginSimpleRequest,
    ) -> Optional[SuccessAuth]:
        ...