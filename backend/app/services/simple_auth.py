from typing import Optional

from app.db.models import DBUser
from app.db.uow import BaseUnitOfWork
from app.schemas.auth import LoginSimpleRequest, SuccessAuth
from app.core.security.abc_jwt_service import BaseJWTService
from app.services.abc import BaseSimpleAuthService
from app.exceptions.auth import NotFoundException


class SimpleAuthService(BaseSimpleAuthService):
    async def authenticate(
            self,
            uow: BaseUnitOfWork,
            jwt_service: BaseJWTService,
            login_data: LoginSimpleRequest
    ) -> Optional[SuccessAuth]:
        if not login_data:
            raise NotFoundException()

        async with uow:
            return await self._authenticate_user(uow, jwt_service, login_data.model_dump())

    async def _authenticate_user(
            self,
            uow: BaseUnitOfWork,
            jwt_service: BaseJWTService,
            user_data: dict
    ) -> SuccessAuth:
        user = await self._get_or_create_user(uow, user_data)
        return SuccessAuth(access_token=jwt_service.create_access_token(user.id))

    async def _get_or_create_user(
            self,
            uow: BaseUnitOfWork,
            user_data: dict
    ) -> DBUser:
        first_name = user_data.get("name")
        if not first_name:
            raise NotFoundException()

        user = await uow.users.create(self._create_db_user_from_user_data(user_data))

        return user

    def _create_db_user_from_user_data(self, user_data: dict) -> DBUser:
        return DBUser(
            first_name=user_data.get("name"),
        )