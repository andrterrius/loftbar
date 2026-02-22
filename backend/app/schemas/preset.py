from uuid import UUID
from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, field_validator


class FlavorInPreset(BaseModel):
    """Схема для вкуса внутри пресета (при создании/обновлении)"""
    flavor_id: UUID
    percent: float = Field(..., ge=0, le=100, description="Процент вкуса от 0 до 100")


class PresetBase(BaseModel):
    """Базовые поля пресета"""
    name: str
    category: str
    price: float
    description: Optional[str] = None
    image_url: Optional[str] = None

class PresetCreate(PresetBase):
    """Схема для создания пресета"""
    liquid_id: Optional[UUID] = None
    bowl_id: Optional[UUID] = None
    flavors: List[FlavorInPreset]

    @field_validator('flavors')
    @classmethod
    def validate_flavors_not_empty(cls, v: List[FlavorInPreset]) -> List[FlavorInPreset]:
        """Проверка, что список вкусов не пустой"""
        if not v:
            raise ValueError('Вкусы не найдены')
        return v

    @field_validator('flavors')
    @classmethod
    def validate_flavors_percent_sum(cls, v: List[FlavorInPreset]) -> List[FlavorInPreset]:
        """Проверка, что сумма процентов равна 100"""
        if v:
            total_percent = sum(flavor.percent for flavor in v)
            if abs(total_percent - 100) > 0.01:
                raise ValueError(f'Сумма процентов вкусов может быть максимум 100%, у вас {total_percent}%')
        return v

class PresetUpdate(BaseModel):
    """Схема для обновления пресета (все поля опциональны)"""
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    liquid_id: Optional[UUID] = None
    bowl_id: Optional[UUID] = None
    flavors: Optional[List[FlavorInPreset]] = None

class FlavorDetail(FlavorInPreset):
    """Детальная информация о вкусе в пресете"""
    flavor_name: str


class PresetOut(PresetBase):
    """Базовая схема для ответа (список пресетов)"""
    id: UUID
    is_available: bool
    liquid_id: Optional[UUID]
    bowl_id: Optional[UUID]
    liquid_name: Optional[str] = None
    liquid_available: Optional[bool] = None
    bowl_name: Optional[str] = None
    bowl_available: Optional[bool] = None
    flavors: List[FlavorDetail] = []

    model_config = ConfigDict(from_attributes=True)