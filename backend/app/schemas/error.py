from pydantic import BaseModel
from typing import Optional, Dict, Any

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_type: str
    details: Optional[Dict[str, Any]] = None
    field: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Описание ошибки",
                "error_type": "_error",
                "details": {"additional": "info"},
                "field": "field_name"
            }
        }