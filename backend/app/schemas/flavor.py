from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional, List
from datetime import datetime

class FlavorCategoryOut(BaseModel):
    id: UUID4
    name: str

    model_config = ConfigDict(from_attributes=True)

class FlavorBase(BaseModel):
    name: str = Field(..., max_length=64, description="Название вкуса")
    brand: str = Field(..., max_length=64, description="Бренд")
    description: Optional[str] = Field(None, max_length=64, description="Описание")
    categories: Optional[List[FlavorCategoryOut]] = Field(None, description="ID категорий")
    hex_color: Optional[str] = Field(None, max_length=32, description="Цвет в HEX")
    image_url: Optional[str] = Field(None, max_length=255, description="URL изображения")

    model_config = ConfigDict(from_attributes=True)

class FlavorCreate(FlavorBase):
    categories: Optional[List[UUID4]] = Field(None, description="ID категорий")
    priority: Optional[int] = Field(None, description="Приоритет вкуса")

class FlavorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=64)
    brand: Optional[str] = Field(None, max_length=64)
    description: Optional[str] = Field(None, max_length=64)
    categories: Optional[List[UUID4]] = Field(None, description="ID категорий")
    hex_color: Optional[str] = Field(None, max_length=32)
    image_url: Optional[str] = Field(None, max_length=255)
    is_available: Optional[bool] = Field(None, description="Доступность вкуса")
    priority: Optional[int] = Field(None, description="Приоритет вкуса")

class FlavorOut(FlavorBase):
    id: UUID4
    is_available: bool
    priority: Optional[int]

    model_config = ConfigDict(from_attributes=True)
