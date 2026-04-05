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
        phone_number = user_data.get("phone_number")
        if not first_name or not phone_number:
            raise NotFoundException()

        user = await uow.users.get_or_create_by_phone_number(phone_number, first_name)
        return user