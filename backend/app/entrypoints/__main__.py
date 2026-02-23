from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka

from app.di.provider import MainProvider
from app.admin import get_admin_app

from app.core.config import Config, create_config
from app.api import include_routers
from dishka.integrations.fastapi import FastapiProvider
from dishka import make_async_container

config = create_config()

app = FastAPI(
     title="LoftBar",
     summary=(
          "Telegram Mini App for hookah bar orders"
     ),
     version="1.0.0",
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

include_routers(app)

container = make_async_container(MainProvider(), FastapiProvider(), context={Config: config})
admin = get_admin_app(
    app,
    admin_config=config.admin,
    dishka_container=container,
    postgres_dsn=config.postgres.build_dsn(),
    secret_key=config.security.session_secret_key.get_secret_value()
)

setup_dishka(container=container, app=app)