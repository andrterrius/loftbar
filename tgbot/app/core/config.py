from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

class BackendConfig(BaseSettings, env_prefix="BACKEND_"):
    url: str = "http://backend"
    api_v: str = "/api/v1"
    port: int

class CommonConfig(BaseSettings, env_prefix="COMMON_"):
    bot_token: SecretStr
    bot_secret_key: SecretStr

class Config(BaseModel):
    backend: BackendConfig
    common: CommonConfig


def create_config() -> Config:
    return Config(
        backend=BackendConfig(),
        common=CommonConfig()
    )

config = create_config()
