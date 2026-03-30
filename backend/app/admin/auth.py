import time

from app.db.uow import BaseUnitOfWork

from dishka import AsyncContainer

from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request

from app.core.config import AdminConfig


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str,  admin_config: AdminConfig,
                 dishka_container: AsyncContainer,
                 session_lifetime: int = 86400):
        super().__init__(secret_key)
        self._secret_key = secret_key
        self._admin_config = admin_config
        self._dishka_container = dishka_container
        self._session_lifetime = session_lifetime

    async def login(self, request: Request) -> bool:
        form = await request.form()
        login = form.get("login")
        password = form.get("password")
        if login == self._admin_config.login.get_secret_value() and password == self._admin_config.password.get_secret_value():
            request.session.update({
                "sub": login,
                "iat": time.time(),
                "exp": time.time() + self._session_lifetime
            })
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        sub = request.session.get("sub")
        iat = request.session.get("iat")
        exp = request.session.get("exp")

        if not sub or not iat or not exp:
            return False

        if time.time() > exp:
            await self.logout(request)
            return False

        return sub == self._admin_config.login.get_secret_value()