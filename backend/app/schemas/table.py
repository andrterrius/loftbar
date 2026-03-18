from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class TableBase(BaseModel):
    number: int = Field(..., ge=1, description="Номер столика")
    name: Optional[str] = Field(None, max_length=64, description="Название столика")
    seats: int = Field(4, ge=1, le=20, description="Количество мест")
    is_available: bool = Field(True, description="Доступен ли столик")
    location: Optional[str] = Field(None, max_length=50, description="Расположение")
    description: Optional[str] = Field(None, max_length=255, description="Описание")

    model_config = ConfigDict(from_attributes=True)