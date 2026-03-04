from typing import Any, Optional
from uuid import UUID
from .base import BaseServiceException

class OrderServiceException(BaseServiceException):
    """Базовое исключение для сервиса заказов"""
    pass

class TableNotFoundException(OrderServiceException):
    """Столик не найден"""
    def __init__(self, table_id: Any):
        super().__init__(
            message=f"Столик с ID {table_id} не найден",
            details={"table_id": str(table_id)}
        )

class PresetNotFoundException(OrderServiceException):
    """Пресет не найден"""
    def __init__(self, preset_id: Any):
        super().__init__(
            message=f"Пресет с ID {preset_id} не найден",
            details={"preset_id": str(preset_id)}
        )

class PresetUnavailableException(OrderServiceException):
    """Пресет недоступен"""
    def __init__(self, preset_name: str):
        super().__init__(
            message=f"Пресет '{preset_name}' недоступен",
            details={"preset_name": preset_name}
        )

class LiquidNotFoundException(OrderServiceException):
    def __init__(self, liquid_id: UUID):
        super().__init__(
            message="Жидкость не найдена",
            details={"liquid_id": str(liquid_id)}
        )

class BowlNotFoundException(OrderServiceException):
    def __init__(self, bowl_id: UUID):
        super().__init__(
            message="Чаша не найдена",
            details={"bowl_id": str(bowl_id)}
        )

class BowlUnavailableException(OrderServiceException):
    def __init__(self, bowl_name: str):
        super().__init__(f"Чаша '{bowl_name}' недоступна")

class FlavorNotFoundException(OrderServiceException):
    def __init__(self, flavor_id: UUID):
        super().__init__(
            message="Вкус не найден",
            details={"flavor_id": str(flavor_id)}
        )

class FlavorUnavailableException(OrderServiceException):
    def __init__(self, flavor_name: str):
        super().__init__(f"Вкус '{flavor_name}' недоступен")

class OrderCreateException(OrderServiceException):
    """Не удалось сделать заказ"""
    def __init__(self):
        super().__init__(
            message=f"Не удалось сделать заказ",
            details={}
        )