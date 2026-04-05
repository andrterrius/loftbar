from fastapi import FastAPI
from sqladmin import Admin

from .admin_router import create_admin_flavor_router, create_admin_preset_router

def include_admin_router(app: FastAPI, admin: Admin) -> None:
    app.include_router(create_admin_flavor_router(admin))
    app.include_router(create_admin_preset_router(admin))