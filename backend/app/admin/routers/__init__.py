from fastapi import FastAPI
from sqladmin import Admin

from .admin_router import create_admin_router

def include_admin_router(app: FastAPI, admin: Admin) -> None:
    router = create_admin_router(admin)
    print(router)
    app.include_router(router)