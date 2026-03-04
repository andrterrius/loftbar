from uuid import UUID
from typing import List, Optional, Sequence

from app.db.uow import BaseUnitOfWork
from app.db.models import DBPreset, DBPresetFlavor
from app.schemas.preset import (
    PresetCreate,
    PresetUpdate,
    PresetOut,
    FlavorInPresetOut,
    BowlOut,
    LiquidOut
)
from app.services.abc.abc_preset import BasePresetService


class PresetService(BasePresetService):
    async def get_all(self, uow: BaseUnitOfWork) -> List[PresetOut]:
        async with uow:
            presets = await uow.presets.get_all_with_relations()
            return [self._preset_to_detail_out(p) for p in presets]

    async def get_available(self, uow: BaseUnitOfWork) -> List[PresetOut]:
        async with uow:
            presets = await uow.presets.get_available_with_relations()
            return [self._preset_to_detail_out(p) for p in presets if p.is_fully_available]

    async def get_by_id(self, uow: BaseUnitOfWork, preset_id: UUID) -> Optional[PresetOut]:
        async with uow:
            return await self.get_by_id_(uow, preset_id)

    async def get_by_id_(self, uow_inited: BaseUnitOfWork, preset_id: UUID) -> Optional[PresetOut]:
        preset = await uow_inited.presets.get_with_relations(preset_id)
        if not preset:
            return None
        return self._preset_to_detail_out(preset)

    async def create(self, uow: BaseUnitOfWork, data: PresetCreate, created_by_id: UUID = None) -> PresetOut:
        async with uow:
            return await self.create_(uow, data, created_by_id)

    async def create_(self, uow_inited: BaseUnitOfWork, data: PresetCreate, created_by_id: UUID = None) -> PresetOut:
        preset = DBPreset(
            name=data.name,
            is_available=data.is_available,
            description=data.description,
            hex_color=data.hex_color,
            category=data.category,
            liquid_id=data.liquid_id,
            bowl_id=data.bowl_id,
            created_by_id=created_by_id
        )
        await uow_inited.presets.create(preset)

        for flavor in data.flavors:
            await uow_inited.presets.add_flavor_to_preset(
                preset_id=preset.id,
                flavor_id=flavor.flavor_id,
                percent=flavor.percent
            )
        preset_with_rels = await uow_inited.presets.get_with_relations(preset.id)
        return self._preset_to_detail_out(preset_with_rels)


    async def update(self, uow: BaseUnitOfWork, preset_id: UUID, data: PresetUpdate) -> Optional[PresetOut]:

        async with uow:
            preset = await uow.presets.get_by_id(preset_id)
            if not preset:
                return None

            update_data = data.model_dump(exclude_unset=True, exclude={'flavors'})
            for field, value in update_data.items():
                setattr(preset, field, value)

            if data.flavors is not None:
                current_flavors = await uow.presets.get_preset_flavors(preset_id)
                current_map = {str(f.flavor_id): f for f in current_flavors}

                for new_flavor in data.flavors:
                    fid_str = str(new_flavor.flavor_id)
                    if fid_str in current_map:
                        await uow.presets.update_flavor_percent(
                            preset_id, new_flavor.flavor_id, new_flavor.percent
                        )
                        del current_map[fid_str]
                    else:
                        await uow.presets.add_flavor_to_preset(
                            preset_id, new_flavor.flavor_id, new_flavor.percent
                        )

                for old_flavor in current_map.values():
                    await uow.presets.remove_flavor_from_preset(preset_id, old_flavor.flavor_id)

            updated = await uow.presets.get_with_relations(preset_id)
            return self._preset_to_detail_out(updated)

    async def delete(self, uow: BaseUnitOfWork, preset_id: UUID) -> None:
        async with uow:
            await uow.presets.delete(preset_id)


    def _calculate_final_price(self, preset: DBPreset) -> int:
        total_price = preset.settings.preset_base_price
        if preset.liquid and getattr(preset.liquid, 'is_available', True):
            total_price += preset.liquid.price
        if preset.bowl and getattr(preset.bowl, 'is_available', True):
            total_price += preset.bowl.price

        return total_price

    def _preset_to_detail_out(self, preset: DBPreset) -> PresetOut:
        flavors = [FlavorInPresetOut(flavor=pf.flavor, percent=pf.percent) for pf in preset.preset_flavors]

        return PresetOut(
            id=preset.id,
            name=preset.name,
            category=preset.category,
            price=self._calculate_final_price(preset),
            description=preset.description,
            hex_color=preset.hex_color,
            liquid=LiquidOut.model_validate(preset.liquid),
            bowl=BowlOut.model_validate(preset.bowl),
            is_available=preset.is_fully_available,
            flavors=flavors
        )