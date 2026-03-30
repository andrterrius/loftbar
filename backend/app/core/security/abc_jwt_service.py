from typing import Protocol, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Структура payload токена"""
    sub: str
    exp: int
    type: str
    extra: Dict[str, Any] = None


class BaseJWTService(Protocol):
    """
    Протокол (интерфейс) для сервиса работы с JWT токенами
    """

    def create_access_token(self, user_id: UUID, **kwargs) -> str:
        ...
    def verify_token(self, token: str) -> Optional[TokenPayload]:
        ...
