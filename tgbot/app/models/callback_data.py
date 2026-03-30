from typing import Optional
from aiogram.filters.callback_data import CallbackData


class OrderCallback(CallbackData, prefix="order"):
    action: str
    order_id: str
    status: Optional[str] = None