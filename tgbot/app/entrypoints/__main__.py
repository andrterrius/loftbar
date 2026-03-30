import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import config
from app.middlewares.api_middleware import APIMiddleware
from app.handlers import commands, callbacks

logger = logging.getLogger(__name__)


async def main():
    bot_token = config.common.bot_token.get_secret_value()

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )
    dp = Dispatcher()

    dp.message.middleware(APIMiddleware())
    dp.callback_query.middleware(APIMiddleware())

    commands.register_commands(dp)
    callbacks.register_callbacks(dp)

    logger.info(f"Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())