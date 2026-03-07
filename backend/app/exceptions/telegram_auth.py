from .base import BaseTelegramAuthException

class InvalidInitDataException(BaseTelegramAuthException):
    """Ошибка авторизации через телеграм init data"""
    def __init__(self):
        super().__init__(
            message="Ошибка авторизации, перезайдите в приложение!"
        )

class MissedInitDataHeader(BaseTelegramAuthException):
    """Пропущен X-Init-Data header в запросе"""
    def __init__(self):
        super().__init__(
            message="X-Init-Data header пропущен в вашем запросе!"
        )