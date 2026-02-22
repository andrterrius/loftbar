from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork
from app.services.abc import BaseFlavorService
from app.schemas.flavor import FlavorCreate, FlavorUpdate, FlavorOut

flavors_router = APIRouter(
    prefix="/flavors",
    tags=["flavors"],
    route_class=DishkaRoute
)

@flavors_router.post("/", response_model=FlavorOut)
async def create_flavor(
    data: FlavorCreate,
    service: FromDishka[BaseFlavorService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Создать новый вкус"""
    result = await service.create_flavor(uow, data)
    return result

@flavors_router.get("/", response_model=list[FlavorOut])
async def get_all(
    service: FromDishka[BaseFlavorService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Получить список всех вкусов"""
    result = await service.get_all(uow)
    return result

@flavors_router.get("/available", response_model=list[FlavorOut])
async def get_available(
    service: FromDishka[BaseFlavorService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Получить список доступных вкусов"""
    result = await service.get_available(uow)
    return result

@flavors_router.get("/{flavor_id}", response_model=FlavorOut)
async def get_flavor(
    flavor_id: UUID,
    service: FromDishka[BaseFlavorService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Получить конкретный вкус по ID"""
    result = await service.get_flavor_by_id(uow, flavor_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Вкус не найден")
    return result

@flavors_router.patch("/{flavor_id}", response_model=FlavorOut)
async def update_flavor(
    flavor_id: UUID,
    data: FlavorUpdate,
    service: FromDishka[BaseFlavorService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Обновить данные вкуса"""
    result = await service.update_flavor(uow, flavor_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Вкус не найден")
    return result

@flavors_router.delete("/{flavor_id}", status_code=204)
async def delete_flavor(
    flavor_id: UUID,
    service: FromDishka[BaseFlavorService],
    uow: FromDishka[BaseUnitOfWork],
):
    """Удалить вкус"""
    deleted = await service.delete_flavor(uow, flavor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Вкус не найден")
    return Response(status_code=204)