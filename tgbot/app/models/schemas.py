from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import OrderStatus


class OrderStatusUpdate(BaseModel):
    id: UUID
    status: OrderStatus


class OrderStatusUpdateTelegram(OrderStatusUpdate):
    chat_id: int
    message_id: int


class UserBase(BaseModel):
    telegram_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = False
    is_active: Optional[bool] = True
    is_banned: Optional[bool] = False
    is_admin: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    telegram_id: Optional[int] = None


class UserResponse(UserBase):
    id: UUID
    is_admin: bool
    created_at: datetime
    updated_at: datetime