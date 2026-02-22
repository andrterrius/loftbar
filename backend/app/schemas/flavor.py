from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional

class FlavorBase(BaseModel):
    name: str = Field(..., max_length=64, description="Название вкуса")
    brand: str = Field(..., max_length=64, description="Бренд")
    category: str = Field(..., max_length=32, description="Категория")
    hex_color: Optional[str] = Field(None, max_length=32, description="Цвет в HEX")
    image_url: Optional[str] = Field(None, max_length=255, description="URL изображения")

class FlavorCreate(FlavorBase):
    pass  # все поля уже определены в FlavorBase

class FlavorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=64)
    brand: Optional[str] = Field(None, max_length=64)
    category: Optional[str] = Field(None, max_length=32)
    hex_color: Optional[str] = Field(None, max_length=32)
    image_url: Optional[str] = Field(None, max_length=255)
    is_available: Optional[bool] = Field(None, description="Доступность вкуса")

class FlavorOut(FlavorBase):
    id: UUID4
    is_available: bool

    model_config = ConfigDict(from_attributes=True)