import os

from fastapi import FastAPI
from dishka import AsyncContainer
from sqladmin import Admin, ModelView
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine

from .auth import AdminAuth

from app.core.config import AdminConfig

from .models import (
    BowlAdmin,
    FlavorAdmin,
    LiquidAdmin,
    PresetAdmin,
    UserAdmin,
)

_views = [
    PresetAdmin,
    BowlAdmin,
    FlavorAdmin,
    LiquidAdmin,
    UserAdmin,
]

def get_admin_app(app: FastAPI, admin_config: AdminConfig, dishka_container: AsyncContainer, postgres_dsn: str, secret_key: str):
    authentication_backend = AdminAuth(secret_key=secret_key, admin_config=admin_config, dishka_container=dishka_container)
    BASE_DIR = Path(__file__).parent
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
    admin = Admin(app, create_async_engine(postgres_dsn), authentication_backend=authentication_backend, templates_dir=TEMPLATES_DIR, base_url="/admin")
    for view in _views:
        admin.add_model_view(view)
    return admin