from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import inject
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from fastapi import Request, HTTPException
from typing import Optional
from telegram_init_data import validate, parse, TelegramInitDataError, InitData
from app.core.config import Config
from app.services.abc import BaseTgAuthService
from app.services import TgAuthService
from app.exceptions.telegram_auth import (
    InvalidInitDataException,
    MissedInitDataHeader,
    InvalidBotSecretException
)

from app.schemas.tgbot import TgBotAuthInfo

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
            return None

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

    @provide(scope=Scope.REQUEST)
    def tg_bot_check_auth(
            self,
            request: Request,
            config: Config,
    ) -> TgBotAuthInfo:
        init_data_header = request.headers.get("X-BOT-SECRET")
        if init_data_header != config.common.bot_secret_key.get_secret_value():
            raise InvalidBotSecretException()

        return TgBotAuthInfo(is_authenticated=True)

    @provide(scope=Scope.APP, provides=Bot)
    def get_tg_bot(self, config: Config) -> Bot:
        return Bot(
            config.common.bot_token.get_secret_value(),
            default=DefaultBotProperties(
                parse_mode="HTML",
                link_preview_is_disabled=True
            )
        )