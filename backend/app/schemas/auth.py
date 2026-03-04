from pydantic import BaseModel
from uuid import UUID

class TokenPayload(BaseModel):
    sub: str
    exp: int

class CurrentUser(BaseModel):
    id: UUID

class SuccessAuth(BaseModel):
    access_token: str