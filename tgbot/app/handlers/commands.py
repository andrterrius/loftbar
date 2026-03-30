import logging
from typing import Optional

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import hbold

from app.models.schemas import UserResponse

logger = logging.getLogger(__name__)


async def cmd_start(message: types.Message, api_user: Optional[UserResponse]):
    """Обработчик команды /start"""
    if api_user and api_user.first_name:
        name = api_user.first_name
    else:
        name = message.from_user.first_name

    await message.answer(
        f"Привет, {hbold(name)}!\n"
        f"Бот работает и готов обрабатывать заказы."
    )


def register_commands(dp):
    """Регистрация всех команд"""
    dp.message.register(cmd_start, Command("start"))