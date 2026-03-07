from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

class AppConfig(BaseSettings, env_prefix="APP_"):
    domain: str
    production: bool

class CommonConfig(BaseSettings, env_prefix="COMMON_"):
    bot_token: SecretStr
    admins: list[int]

class AdminConfig(BaseSettings, env_prefix="ADMIN_"):
    login: SecretStr
    password: SecretStr

class SecurityConfig(BaseSettings, env_prefix="SECURITY_"):
    session_secret_key: SecretStr
    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    enable_logging: bool = False

    def build_dsn(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        ).render_as_string(hide_password=False)

class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    use_redis: bool = True

    host: str
    port: int
    password: str

class Config(BaseModel):
    common: CommonConfig
    redis: RedisConfig
    postgres: PostgresConfig
    admin: AdminConfig
    security: SecurityConfig
    app: AppConfig


def create_config() -> Config:
    return Config(common=CommonConfig(),
                  redis=RedisConfig(),
                  postgres=PostgresConfig(),
                  admin=AdminConfig(),
                  security=SecurityConfig(),
                  app=AppConfig()
                  )
