import logging
from typing import Optional

import aiohttp
from aiohttp import ClientError

from app.core.config import config
from app.models.schemas import UserCreate, UserResponse, OrderStatusUpdateTelegram

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self):
        self.base_url = f"{config.backend.url}:{config.backend.port}{config.backend.api_v}"
        self.secret_key = config.common.bot_secret_key.get_secret_value()
        self.headers = {
            "X-BOT-SECRET": self.secret_key,
            "Content-Type": "application/json"
        }

    async def send_user_data(self, user_data: UserCreate) -> Optional[UserResponse]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                        f"{self.base_url}/tgbot",
                        json=user_data.model_dump(exclude_none=True),
                        headers=self.headers
                ) as response:
                    if response.status == 200:
                        user_response = await response.json()
                        logger.info(f"User data sent successfully: {user_response}")
                        return UserResponse(**user_response)
                    else:
                        logger.error(f"API error: {response.status}")
                        return None
            except ClientError as e:
                logger.error(f"Failed to send user data: {e}")
                return None

    async def update_order_status(self, order_update: OrderStatusUpdateTelegram) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        f"{self.base_url}/tgbot/order/status",
                        json=order_update.model_dump(mode="json"),
                        headers=self.headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Order status updated successfully: {result}")
                        return True
                    else:
                        logger.error(f"Failed to update order status: {response.status}")
                        return False
            except ClientError as e:
                logger.error(f"API request failed: {e}")
                return False