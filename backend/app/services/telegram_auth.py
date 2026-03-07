from typing import Optional
from telegram_init_data import InitData

from app.db.models import DBUser
from app.db.uow import BaseUnitOfWork
from app.schemas.auth import SuccessAuth
from app.core.security.abc_jwt_service import BaseJWTService
from app.services.abc import BaseTgAuthService
from app.exceptions.telegram_auth import InvalidInitDataException


class TgAuthService(BaseTgAuthService):
    async def authenticate(
            self,
            uow: BaseUnitOfWork,
            jwt_service: BaseJWTService,
            init_data: InitData
    ) -> Optional[SuccessAuth]:
        if not init_data or not init_data.get("user"):
            raise InvalidInitDataException()

        async with uow:
            return await self._authenticate_user(uow, jwt_service, init_data["user"])

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
        telegram_id = user_data.get("id")
        if not telegram_id:
            raise InvalidInitDataException()

        user = await uow.users.get_by_telegram_id(telegram_id)

        if not user:
            user = await uow.users.create(self._create_db_user_from_telegram_data(user_data))
        else:
            if user.is_active is not user_data.get("allows_write_to_pm"):
                user.is_active = user_data.get("allows_write_to_pm", False)

        return user

    def _create_db_user_from_telegram_data(self, user_data: dict) -> DBUser:
        return DBUser(
            telegram_id=user_data.get("id"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            username=user_data.get("username"),
            photo_url=user_data.get("photo_url"),
            is_premium=user_data.get("is_premium", False),
            is_active=user_data.get("allows_write_to_pm", True),
        )