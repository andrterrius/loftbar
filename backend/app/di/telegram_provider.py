from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import inject
from fastapi import Request, HTTPException
from typing import Optional
from telegram_init_data import validate, parse, TelegramInitDataError, InitData
from app.core.config import Config  # ваш класс конфига
from app.services.abc import BaseTgAuthService
from app.services import TgAuthService
from app.exceptions.telegram_auth import InvalidInitDataException, MissedInitDataHeader


class TelegramProvider(Provider):
    """
    Провайдер для Telegram Init Data
    """

    @provide(scope=Scope.REQUEST, provides=InitData)
    async def get_telegram_init_data(
            self,
            request: Request,
            config: Config,
    ) -> InitData:
        """
        Простая зависимость для получения и валидации Telegram Init Data
        """
        init_data_header = request.headers.get("X-Init-Data")

        if not init_data_header:
            raise MissedInitDataHeader()

        try:
            validate(
                init_data_header,
                config.common.bot_token.get_secret_value()
            )

            return parse(init_data_header)
        except:
            raise InvalidInitDataException()

    @provide(scope=Scope.REQUEST, provides=BaseTgAuthService)
    def get_tg_auth_service(self) -> TgAuthService:
        return TgAuthService()