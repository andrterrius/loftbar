from .liquid import LiquidOut
from .flavor import FlavorOut
from .bowl import BowlOut

from uuid import UUID
from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, field_validator


class FlavorInPreset(BaseModel):
    """Схема для вкуса внутри пресета (при создании/обновлении)"""
    flavor_id: UUID
    percent: float = Field(..., ge=0, le=100, description="Процент вкуса от 0 до 100")

class FlavorInPresetOut(BaseModel):
    """Выходная информация о вкусе в пресете"""
    flavor: FlavorOut
    percent: float = Field(..., ge=0, le=100, description="Процент вкуса от 0 до 100")

class PresetBase(BaseModel):
    """Базовые поля пресета"""
    name: str
    category: str
    strength: int = 1
    is_available: bool = True
    description: Optional[str] = None
    hex_color: Optional[str] = None

class PresetCreate(PresetBase):
    """Схема для создания пресета"""
    liquid_id: Optional[UUID] = None
    bowl_id: Optional[UUID] = None
    strength: int = 1
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
    def validate_flavors_unique(cls, v: List[FlavorInPreset]) -> List[FlavorInPreset]:
        """Проверка, что список вкусов не пустой"""
        flavor_ids = [item.flavor_id for item in v]
        if len(flavor_ids) != len(set(flavor_ids)):
            raise ValueError('Вкусы не могут повторяться несколько раз')
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

    @field_validator('strength')
    @classmethod
    def validate_strength_range(cls, v: int) -> int:
        """Проверка, strength в пределах от 1 до 10"""
        if v:
            if not (1 <= v <= 10):
                raise ValueError(f'Крепкость может быть только в интервале от 1 до 10 включительно')
        return v

class PresetCreateInOrder(BaseModel):
    """Схема для создания пресета"""
    liquid_id: Optional[UUID] = None
    bowl_id: Optional[UUID] = None
    strength: int = 1
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
    def validate_flavors_unique(cls, v: List[FlavorInPreset]) -> List[FlavorInPreset]:
        """Проверка, что список вкусов не пустой"""
        flavor_ids = [item.flavor_id for item in v]
        if len(flavor_ids) != len(set(flavor_ids)):
            raise ValueError('Вкусы не могут повторяться несколько раз')
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

    @field_validator('strength')
    @classmethod
    def validate_strength_range(cls, v: int) -> int:
        """Проверка, strength в пределах от 1 до 10"""
        if v:
            if not (1 <= v <= 10):
                raise ValueError(f'Крепкость может быть только в интервале от 1 до 10 включительно')
        return v

class PresetUpdate(PresetCreate):
    """Схема для обновления пресета"""
    pass

class PresetOut(PresetBase):
    """Базовая схема для ответа (список пресетов)"""
    id: UUID
    price: Optional[float] = None
    is_available: bool
    strength: int
    bowl: BowlOut
    liquid: LiquidOut
    flavors: List[FlavorInPresetOut] = []

    model_config = ConfigDict(from_attributes=True)

class PresetHistoryOut(PresetBase):
    """Базовая схема для ответа (список пресетов)"""
    id: UUID
    price: float
    is_available: bool
    strength: int
    bowl: str
    liquid: str
    flavors: List[FlavorInPresetOut] = []

    model_config = ConfigDict(from_attributes=True)

class PresetsEditOut(BaseModel):
    presets: List[PresetOut]

class PresetEditData(BaseModel):
    preset: PresetOut
    liquids: List[LiquidOut]
    flavors: List[FlavorOut]
    bowls: List[BowlOut]


class PresetBasePrice(BaseModel):
    base_price: float
    strength_added_price: float

    model_config = ConfigDict(from_attributes=True)