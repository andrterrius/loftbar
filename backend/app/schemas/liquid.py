from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional

class LiquidBase(BaseModel):
    name: str = Field(..., max_length=64, description="Название жидкости")
    category: str = Field(..., max_length=32, description="Категория")
    price: float = Field(..., description="Цена в рублях")
    hex_color: Optional[str] = Field(None, max_length=32, description="Цвет в HEX")

class LiquidOut(LiquidBase):
    id: UUID4
    is_available: bool

    model_config = ConfigDict(from_attributes=True)