from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    telegram_id: Optional[int] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: bool = False
    is_active: bool = True
    is_banned: bool = False
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    """Схема для создания пользователя"""
    telegram_id: Optional[int] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: bool = False
    is_active: bool = True


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    first_name: Optional[str] = None
    phone_number: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    is_active: Optional[bool] = None
    is_banned: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserResponse(UserBase):
    """Схема для ответа с данными пользователя"""
    id: UUID
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserMeOut(BaseModel):
    """Схема для ответа пользователю"""
    phone_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)