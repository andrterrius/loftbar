import uuid
from uuid import UUID
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
from app.services.abc import BasePresetService, BaseFlavorService, BaseBowlService, BaseLiquidService

from app.schemas.preset import PresetUpdate, PresetCreate
from app.schemas.flavor import FlavorUpdate, FlavorCreate


def create_admin_middleware_dependency(admin: Admin):
    """Создает зависимость для применения middleware к роутеру"""

    async def admin_middleware_dependency(request: Request):
        if await admin.authentication_backend.authenticate(request):
            request.state.admin = admin
            return request
        else:
            raise HTTPException(status_code=302, headers={"Location": "/admin"})

    return admin_middleware_dependency

def create_admin_preset_router(admin: Admin):
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
            bowl_service: FromDishka[BaseBowlService],
            liquid_service: FromDishka[BaseLiquidService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Создание нового пресета"""
        admin: Admin = request.state.admin

        flavors = await flavor_service.get_all(uow)
        bowls = await bowl_service.get_all(uow)
        liquids = await liquid_service.get_all(uow)

        return templates.TemplateResponse(
            "preset/edit.html",
            {
                "admin": admin,
                "request": request,
                "obj": None,
                "liquids": liquids,
                "bowls": bowls,
                "flavors": flavors,
            }
        )

    @router.get("/edit/{preset_id}", response_class=HTMLResponse)
    async def edit_preset(
            request: Request,
            preset_id: UUID,
            preset_service: FromDishka[BasePresetService],
            flavor_service: FromDishka[BaseFlavorService],
            bowl_service: FromDishka[BaseBowlService],
            liquid_service: FromDishka[BaseLiquidService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Редактирование существующего пресета"""
        admin: Admin = request.state.admin

        obj = await preset_service.get_by_id(uow, preset_id)
        flavors = await flavor_service.get_all(uow)
        bowls = await bowl_service.get_all(uow)
        liquids = await liquid_service.get_all(uow)

        return templates.TemplateResponse(
            "preset/edit.html",
            {
                "admin": admin,
                "request": request,
                "obj": obj,
                "liquids": liquids,
                "bowls": bowls,
                "flavors": flavors,
            }
        )

    @router.post("/save")
    async def insert_preset(
            request: Request,
            data: PresetCreate,
            preset_service: FromDishka[BasePresetService],
            uow: FromDishka[BaseUnitOfWork]
    ):
        """Сохранение пресета"""

        admin: Admin = request.state.admin
        result = await preset_service.create(uow, data)

        return RedirectResponse(url="/admin/db-preset/list", status_code=302)

    @router.put("/save/{preset_id}")
    async def update_preset(
            request: Request,
            preset_id: UUID,
            data: PresetUpdate,
            preset_service: FromDishka[BasePresetService],
            uow: FromDishka[BaseUnitOfWork]
    ):
        """Сохранение пресета"""
        print(data)
        admin: Admin = request.state.admin
        result = await preset_service.update(uow, preset_id, data)
        if not result:
            raise HTTPException(status_code=404, detail="Preset not found")

    return router


def create_admin_flavor_router(admin: Admin):
    admin_middleware = create_admin_middleware_dependency(admin)
    templates = Jinja2Templates(directory="app/admin/templates")

    router = APIRouter(
        prefix="/admin/db-flavor",
        include_in_schema=False,
        dependencies=[Depends(admin_middleware)],
        route_class=DishkaRoute
    )

    @router.get("/create", response_class=HTMLResponse)
    async def create_flavor(
            request: Request,
            flavor_service: FromDishka[BaseFlavorService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Создание нового вкуса"""
        admin: Admin = request.state.admin

        categories = await flavor_service.get_all_categories(uow)

        return templates.TemplateResponse(
            "flavor/edit.html",
            {
                "admin": admin,
                "request": request,
                "obj": None,
                "categories": categories
            }
        )

    @router.get("/edit/{flavor_id}", response_class=HTMLResponse)
    async def edit_flavor(
            request: Request,
            flavor_id: UUID,
            flavor_service: FromDishka[BaseFlavorService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Редактирование существующего вкуса"""
        admin: Admin = request.state.admin

        obj = await flavor_service.get_flavor_by_id(uow, flavor_id)
        categories = await flavor_service.get_all_categories(uow)
        return templates.TemplateResponse(
            "flavor/edit.html",
            {
                "admin": admin,
                "request": request,
                "obj": obj,
                "categories": categories
            }
        )

    @router.post("/save", response_class=HTMLResponse)
    async def insert_flavor(
            data: FlavorCreate,
            flavor_service: FromDishka[BaseFlavorService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Сохранение вкуса"""
        result = await flavor_service.create_flavor(uow, data)
        return RedirectResponse(url="/admin/db-flavor/list", status_code=302)

    @router.put("/save/{flavor_id}", response_class=HTMLResponse)
    async def update_flavor(
            flavor_id: UUID,
            data: FlavorUpdate,
            flavor_service: FromDishka[BaseFlavorService],
            uow: FromDishka[BaseUnitOfWork],
    ):
        """Обновление вкуса"""

        result = await flavor_service.update_flavor(uow, flavor_id, data)
        if not result:
            raise HTTPException(status_code=404, detail="Flavor not found")

        return RedirectResponse(url="/admin/db-flavor/list", status_code=302)

    return router