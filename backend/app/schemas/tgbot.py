from pydantic import ConfigDict, BaseModel, Field, field_validator

class TgBotAuthInfo(BaseModel):
    is_authenticated: bool
    client_type: str = "bot"
