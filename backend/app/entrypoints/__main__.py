from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://andrterrius.lol",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


container = make_async_container(MainProvider(), FastapiProvider(), context={Config: config})
admin = get_admin_app(
    app,
    admin_config=config.admin,
    dishka_container=container,
    postgres_dsn=config.postgres.build_dsn(),
    secret_key=config.security.session_secret_key.get_secret_value()
)

setup_dishka(container=container, app=app)