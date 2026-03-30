from pydantic import BaseModel, Field
from uuid import UUID

class TokenPayload(BaseModel):
    sub: str
    exp: int

class CurrentUser(BaseModel):
    id: UUID

class SuccessAuth(BaseModel):
    access_token: str

class LoginSimpleRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")