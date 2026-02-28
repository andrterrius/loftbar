import uuid
from fastapi import HTTPException, APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqladmin import Admin
from typing import List, Optional

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BasePresetService, BaseFlavorService

from app.schemas.preset import PresetUpdate, PresetCreate

def create_admin_middleware_dependency(admin: Admin):
    """Создает зависимость для применения middleware к роутеру"""

    async def admin_middleware_dependency(request: Request):
        if await admin.authentication_backend.authenticate(request):
            request.state.admin = admin
            return request
        else:
            raise HTTPException(status_code=302, headers={"Location": "/admin"})

    return admin_middleware_dependency

class MockItem:
    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

def get_mock_data():
    """Создает мок-данные для тестирования"""
    return {
        "liquids": [
            MockItem(uuid.uuid4(), "Малиновый лимонад", category="фруктовый", is_available=True, price=299.99),
            MockItem(uuid.uuid4(), "Клубничный чизкейк", category="десертный", is_available=True, price=349.99),
            MockItem(uuid.uuid4(), "Мятная свежесть", category="мятный", is_available=False, price=279.99),
        ],
        "bowls": [
            MockItem(uuid.uuid4(), "Стандартная чаша", category="стандартная", is_available=True, price=199.99),
            MockItem(uuid.uuid4(), "Премиум чаша", category="премиум", is_available=True, price=399.99),
            MockItem(uuid.uuid4(), "Стеклянная чаша", category="стекло", is_available=False, price=599.99),
        ]
    }

def create_admin_router(admin: Admin):
    admin_middleware = create_admin_middleware_dependency(admin)
    templates = Jinja2Templates(directory="app/admin/templates")

    router = APIRouter(
        prefix="/admin/db-preset",
        include_in_schema=False,
        dependencies=[Depends(admin_middleware)],
        route_class=DishkaRoute
    )


    @router.get("/create", response_class=HTMLResponse)
    async def create_preset(
            request: Request,
            preset_service: FromDishka[BasePresetService],
            flavor_service: FromDishka[BaseFlavorService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Создание нового пресета"""
        admin: Admin = request.state.admin
        mock_data = get_mock_data()

        flavors = await flavor_service.get_available(uow)

        return templates.TemplateResponse(
            "preset/edit.html",
            {
                "admin": admin,
                "request": request,
                "obj": None,
                "liquids": mock_data["liquids"],
                "bowls": mock_data["bowls"],
                "flavors": flavors,
            }
        )

    @router.get("/edit/{preset_id}", response_class=HTMLResponse)
    async def edit_preset(
            request: Request,
            preset_id: str,
            preset_service: FromDishka[BasePresetService],
            flavor_service: FromDishka[BaseFlavorService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Редактирование существующего пресета"""

        mock_data = get_mock_data()
        admin: Admin = request.state.admin

        obj = await preset_service.get_by_id(uow, preset_id)
        flavors = await flavor_service.get_all(uow)

        return templates.TemplateResponse(
            "preset/edit.html",
            {
                "admin": admin,
                "request": request,
                "obj": obj,
                "liquids": mock_data["liquids"],
                "bowls": mock_data["bowls"],
                "flavors": flavors,
            }
        )

    @router.post("/save")
    async def insert_preset(
            request: Request,
            data: PresetCreate,
    ):
        """Сохранение пресета"""

        admin: Admin = request.state.admin

        print(data)
        return RedirectResponse(url="/admin/db-preset/list", status_code=302)

    @router.put("/save/{preset_id}")
    async def update_preset(
            request: Request,
            preset_id: str,
            data: PresetUpdate,
    ):
        """Сохранение пресета"""

        admin: Admin = request.state.admin

        print(data)
        # Перенаправляем обратно в список пресетов
        return RedirectResponse(url="/admin/db-preset/list", status_code=302)

    return router