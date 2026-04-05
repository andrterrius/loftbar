from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class SettingsBase(BaseModel):
    preset_base_price: float = Field(0, ge=0, description="Базовая цена пресета")
    strength_added_price: float = Field(0, ge=0, description="Цена за добавление крепости")
    liquids_image_url: Optional[str] = Field(None, max_length=64, description="Изображения жидкостей")
    bowls_image_url: Optional[str] = Field(None, max_length=64, description="Изображения чаш")

class SettingsOut(SettingsBase):
    pass

class SettingsImagesOut(BaseModel):
    liquids_image_url: Optional[str] = Field(None, max_length=255, description="Изображения жидкостей")
    bowls_image_url: Optional[str] = Field(None, max_length=255, description="Изображения чаш")

    model_config = ConfigDict(from_attributes=True)


class SettingsPriceInfo(BaseModel):
    base_price: float = Field(..., ge=0, description="Базовая цена")
    strength_added_price: float = Field(..., ge=0, description="Цена за добавление крепости")