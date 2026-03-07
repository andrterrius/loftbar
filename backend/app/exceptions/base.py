from typing import Any, Optional

class BaseServiceException(Exception):
    """Базовое исключение для сервисов"""
    def __init__(self, message: str, details: Optional[Any] = None, error_type="service_error"):
        self.message = message
        self.details = details
        self.error_type = error_type
        super().__init__(message)

class BaseAuthException(Exception):
    """Базовое исключение для авторизации"""
    def __init__(self, message: str, details: Optional[Any] = None, error_type = "auth_error"):
        self.message = message
        self.details = details
        self.error_type = error_type
        super().__init__(message)

class BaseTelegramAuthException(BaseAuthException):
    """Базовое исключение для авторизации"""
    def __init__(self, message: str, details: Optional[Any] = None, error_type = "telegram_auth_error"):
        super().__init__(message, details, error_type)