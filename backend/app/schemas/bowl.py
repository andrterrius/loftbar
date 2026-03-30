from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional

class BowlBase(BaseModel):
    name: str = Field(..., max_length=64, description="Название чаши")
    category: str = Field(..., max_length=32, description="Категория")
    price: float = Field(..., description="Цена в рублях")
    icon: Optional[str] = Field(None, max_length=32, description="Иконка чаши")

class BowlOut(BowlBase):
    id: UUID4
    is_available: bool

    model_config = ConfigDict(from_attributes=True)