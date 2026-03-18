import logging
from typing import Any, Dict

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from app.services.api_client import APIClient
from app.models.schemas import UserCreate, UserResponse

logger = logging.getLogger(__name__)


class APIMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message | types.CallbackQuery, data: Dict[str, Any]):
        if not isinstance(event, (types.Message, types.CallbackQuery)):
            return await handler(event, data)

        user = event.from_user
        chat_id = event.chat.id if isinstance(event, types.Message) else event.message.chat.id

        user_data = UserCreate(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
            is_premium=user.is_premium
        )

        api_client = APIClient()
        user_response = await api_client.send_user_data(user_data)
        data["api_user"] = user_response
        data["api_client"] = api_client

        return await handler(event, data)