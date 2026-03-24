from dishka import Provider, provide, Scope
from uuid import UUID
from fastapi import Request
from app.core.config import Config
from app.core.security.jwt_service import JWTService
from app.core.security.abc_jwt_service import BaseJWTService
from app.services.abc import BaseSimpleAuthService
from app.services import SimpleAuthService
from app.db.uow import BaseUnitOfWork
from app.schemas.auth import CurrentUser

from app.exceptions.auth import (
    UnauthorizedException,
    MissedHeaderException,
    InvalidSchemaException,
    NotFoundException,
    BannedException
)


class AuthProvider(Provider):

    @provide(scope=Scope.APP, provides=BaseJWTService)
    def get_jwt_service(self, config: Config) -> JWTService:
        return JWTService(
            secret_key=config.security.jwt_secret_key.get_secret_value(),
            algorithm=config.security.jwt_algorithm,
            access_token_expire_minutes=config.security.jwt_expire_minutes
        )

    @provide(scope=Scope.REQUEST, provides=CurrentUser)
    async def get_current_user(
            self,
            request: Request,
            uow: BaseUnitOfWork,
            jwt_service: BaseJWTService) -> CurrentUser:
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise MissedHeaderException()

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid scheme")
        except ValueError:
            raise InvalidSchemaException()

        payload = jwt_service.verify_token(token)
        if not payload:
            raise UnauthorizedException()

        user_id_str = payload.sub
        if not user_id_str:
            raise UnauthorizedException()

        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise UnauthorizedException()

        async with uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise NotFoundException()

            if user.is_banned:
                raise BannedException()

        return CurrentUser(
            id=user_id,
        )

    @provide(scope=Scope.REQUEST, provides=BaseSimpleAuthService)
    async def get_simple_auth_service(self):
        return SimpleAuthService()
