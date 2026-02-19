from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    first_name: str = Field(..., min_length=1, max_length=128, description="Имя")
    last_name: Optional[str] = Field(None, max_length=128, description="Фамилия")
    username: Optional[str] = Field(None, min_length=3, max_length=64, description="Telegram username")
    photo_url: Optional[str] = Field(None, max_length=512, description="URL фото профиля")
    language_code: Optional[str] = Field(None, min_length=2, max_length=10, description="Код языка")
    is_premium: bool = Field(False, description="Премиум статус")