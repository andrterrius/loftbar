from typing import Optional, Any
from .base import BaseAuthException


class InvalidSchemaException(BaseAuthException):
    """Неверный тип"""
    def __init__(self):
        super().__init__(
            message="Используйте Authorization Bearer"
        )

class MissedHeaderException(BaseAuthException):
    """Пропущен Authorization header"""
    def __init__(self):
        super().__init__(
            message="Пропущен Authorization header"
        )

class NotFoundException(BaseAuthException):
    """Пользователь не найден"""
    def __init__(self):
        super().__init__(
            message="Пользователь не найден, перезайдите в приложение!"
        )

class BannedException(BaseAuthException):
    """Заблокирован"""
    def __init__(self):
        super().__init__(
            message="Вы заблокированы!"
        )

class UnauthorizedException(BaseAuthException):
    """Не авторизован"""
    def __init__(self):
        super().__init__(
            message="Вы не авторизованы!"
        )