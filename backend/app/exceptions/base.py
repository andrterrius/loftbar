from typing import Any, Optional


class BaseServiceException(Exception):
    """Базовое исключение для сервисов"""
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(message)