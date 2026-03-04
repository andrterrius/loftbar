from typing import Any, Optional

class BaseServiceException(Exception):
    """Базовое исключение для сервисов"""
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        self.error_type = "service_error"
        super().__init__(message)

class BaseAuthException(Exception):
    """Базовое исключение для авторизации"""
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        self.error_type = "auth_error"
        super().__init__(message)