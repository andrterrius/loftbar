from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka.integrations.fastapi import setup_dishka


from app.core.config import Config, create_config
from app.api import include_routers
from dishka.integrations.fastapi import FastapiProvider
from dishka import make_async_container

from app.di.provider import MainProvider


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

config = create_config()

container = make_async_container(MainProvider(), FastapiProvider(), context={Config: config})

setup_dishka(container=container, app=app)