from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.services.abc import BasePresetService
from app.schemas.preset import PresetCreate, PresetUpdate, PresetOut

presets_router = APIRouter(
    prefix="/presets",
    tags=["presets"],
    route_class=DishkaRoute
)


@presets_router.get("/", response_model=list[PresetOut])
async def get_all_presets(
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Получить все пресеты с флагом is_available"""
    return await service.get_all(uow)


@presets_router.get("/available", response_model=list[PresetOut])
async def get_available_presets(
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Получить только доступные пресеты (is_available=True)"""
    return await service.get_available(uow)


@presets_router.get("/{preset_id}", response_model=PresetOut)
async def get_preset_by_id(
        preset_id: UUID,
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Получить детальную информацию о пресете по ID"""
    preset = await service.get_by_id(uow, preset_id)
    if not preset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preset not found")
    return preset


@presets_router.post("/", response_model=PresetOut, status_code=status.HTTP_201_CREATED)
async def create_preset(
        data: PresetCreate,
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Создать новый пресет"""
    return await service.create(uow, data)


@presets_router.put("/{preset_id}", response_model=PresetOut)
async def update_preset(
        preset_id: UUID,
        data: PresetUpdate,
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Обновить существующий пресет"""
    result = await service.update(uow, preset_id, data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preset not found")
    return result


@presets_router.delete("/{preset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_preset(
        preset_id: UUID,
        service: FromDishka[BasePresetService],
        uow: FromDishka[BaseUnitOfWork],
):
    """Удалить пресет"""
    await service.delete(uow, preset_id)
    return None