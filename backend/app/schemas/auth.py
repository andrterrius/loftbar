import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID

class TokenPayload(BaseModel):
    sub: str
    exp: int

class CurrentUser(BaseModel):
    id: UUID
    preset_base_price: Optional[float]

class SuccessAuth(BaseModel):
    access_token: str

class LoginSimpleRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    phone_number: str = Field(..., description="Номер телефона в международном формате")

    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Валидация номера телефона"""
        if not v:
            raise ValueError('Номер телефона обязателен')

        cleaned = re.sub(r'\D', '', v)

        if not cleaned:
            raise ValueError('Номер телефона должен содержать цифры')

        if len(cleaned) == 10:
            normalized = f'+7{cleaned}'
        elif len(cleaned) == 11:
            if cleaned.startswith('7'):
                normalized = f'+{cleaned}'
            elif cleaned.startswith('8'):
                normalized = f'+7{cleaned[1:]}'
            else:
                raise ValueError('Номер телефона должен начинаться с 7, 8 или +7')
        else:
            raise ValueError('Номер телефона должен содержать 10 или 11 цифр')

        if normalized.startswith('+7'):
            invalid_codes = ['+700', '+701', '+702', '+703', '+704', '+705', '+706', '+707', '+708', '+709']
            if any(normalized.startswith(code) for code in invalid_codes):
                raise ValueError('Некорректный код оператора')

        return normalized