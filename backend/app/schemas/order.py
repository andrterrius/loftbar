from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, Any, Dict, List
from enum import Enum
from .preset import PresetCreateInOrder, PresetOut
from .user import UserBase
from .table import TableBase

class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderCreate(BaseModel):
    """Создание заказа (либо preset_id, либо preset)"""
    table_id: UUID = Field(..., description="ID столика")
    preset_id: Optional[UUID] = Field(None, description="ID готового пресета")
    preset: Optional[PresetCreateInOrder] = Field(None, description="Новый кастомный пресет")
    special_requests: Optional[str] = Field(None, max_length=500)

    @model_validator(mode='after')
    def validate_preset_data(self) -> 'OrderCreate':
        """Проверяем, что указан либо preset_id, либо preset, но не оба"""
        if self.preset_id and self.preset:
            raise ValueError('Нельзя указать одновременно preset_id и preset')
        if not self.preset_id and not self.preset:
            raise ValueError('Необходимо указать либо preset_id, либо preset')
        return self


class OrderStatusUpdate(BaseModel):
    id: UUID
    status: OrderStatus = Field(..., description="Новый статус заказа")

class OrderStatusUpdateTelegram(OrderStatusUpdate):
    chat_id: int
    message_id: int

class OrderUpdate(BaseModel):
    """Обновление данных заказа (для администратора)"""
    id: UUID
    daily_number: Optional[int] = None
    table_id: Optional[UUID] = None
    special_requests: Optional[str] = Field(None, max_length=500)
    status: Optional[OrderStatus] = None
    confirmed_at: Optional[datetime] = None
    ready_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class OrderOutAdmin(BaseModel):
    """Полная информация о заказе для ответа администратору"""
    id: UUID
    daily_number: Optional[int] = None
    preset: Optional[PresetOut] = Field(None, description="Информация о пресете")
    user: Optional[UserBase] = Field(None, description="Информация о пользователе")
    table: Optional[TableBase] = Field(None, description="Информация о столике")
    status: OrderStatus
    total_price: float = Field(..., description="Итоговая цена (рассчитывается в сервисе)")
    special_requests: Optional[str] = None
    is_custom: bool = Field(..., description="True если кастомный заказ")
    custom_name: Optional[str] = Field(None, description="Название кастомного заказа")
    composition_snapshot: Optional[Dict[str, Any]] = Field(
        None,
        description="Снимок состава заказа на момент создания"
    )
    confirmed_at: Optional[datetime] = None
    ready_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    admin_notification_sent: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: UUID
    daily_number: Optional[int] = None

class OrderListItem(BaseModel):
    """Краткая информация о заказе для списков"""
    id: UUID
    status: OrderStatus
    total_price: float
    is_custom: bool
    daily_number: Optional[int] = None
    custom_name: Optional[str] = None
    created_at: datetime
    table_id: Optional[UUID] = None
    user_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)
