import jwt
from datetime import datetime, timedelta, UTC
from typing import Optional, Dict, Any
from uuid import UUID
from .abc_jwt_service import BaseJWTService, TokenPayload

from app.exceptions.auth import UnauthorizedException

class JWTService(BaseJWTService):
    """Реализация JWT сервиса"""

    def __init__(
            self,
            secret_key: str,
            algorithm: str = "HS256",
            access_token_expire_minutes: int = 60
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(
            self,
            user_id: UUID,
            **extra_payload: Dict[str, Any]
    ) -> str:
        """Создание access токена"""
        expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access",
            **extra_payload
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(
            self,
            token: str
    ) -> Optional[TokenPayload]:
        """Верификация токена"""
        try:
            payload_dict = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            extra = {
                k: v for k, v in payload_dict.items()
                if k not in ["sub", "exp", "type"]
            }

            return TokenPayload(
                sub=payload_dict.get("sub"),
                exp=payload_dict.get("exp"),
                type=payload_dict.get("type", "access"),
                extra=extra
            )
        except jwt.PyJWTError:
            raise UnauthorizedException()