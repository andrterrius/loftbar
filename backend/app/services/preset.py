from uuid import UUID
from typing import List, Optional, Sequence

from app.db.uow import BaseUnitOfWork
from app.db.models import DBPreset, DBPresetFlavor
from app.schemas.preset import (
    PresetCreate,
    PresetUpdate,
    PresetOut,
    FlavorDetail
)
from app.services.abc.abc_preset import BasePresetService


class PresetService(BasePresetService):
    async def get_all(self, uow: BaseUnitOfWork) -> List[PresetOut]:
        async with uow:
            presets = await uow.presets.get_all_with_relations()
            return [self._preset_to_detail_out(p) for p in presets]

    async def get_available(self, uow: BaseUnitOfWork) -> List[PresetOut]:
        async with uow:
            presets = await uow.presets.get_all_with_relations()
            return [self._preset_to_detail_out(p) for p in presets if self._is_available(p)]

    async def get_by_id(self, uow: BaseUnitOfWork, preset_id: UUID) -> Optional[PresetOut]:
        async with uow:
            preset = await uow.presets.get_with_relations(preset_id)
            if not preset:
                return None
            return self._preset_to_detail_out(preset)

    async def create(self, uow: BaseUnitOfWork, data: PresetCreate) -> PresetOut:
        async with uow:
            preset = DBPreset(
                name=data.name,
                category=data.category,
                description=data.description,
                liquid_id=data.liquid_id,
                bowl_id=data.bowl_id,
            )
            await uow.presets.create(preset)

            for flavor in data.flavors:
                await uow.presets.add_flavor_to_preset(
                    preset_id=preset.id,
                    flavor_id=flavor.flavor_id,
                    percent=flavor.percent
                )
            preset_with_rels = await uow.presets.get_with_relations(preset.id)
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

    def _is_available(self, preset: DBPreset) -> bool:
        if preset.liquid and not getattr(preset.liquid, 'is_available', True):
            return False
        if preset.bowl and not getattr(preset.bowl, 'is_available', True):
            return False

        final_percent = 0

        for pf in preset.preset_flavors:
            if pf.flavor and not getattr(pf.flavor, 'is_available', True):
                return False
            final_percent += pf.percent

        if final_percent != 100:
            return False

        return preset.is_available

    def _preset_to_detail_out(self, preset: DBPreset) -> PresetOut:
        flavors = [
            FlavorDetail(
                flavor_id=pf.flavor_id,
                percent=pf.percent,
                is_available=pf.flavor.is_available,
                name=pf.flavor.name if pf.flavor else "Unknown",
                brand=pf.flavor.brand if pf.flavor else "Unknown"
            )
            for pf in preset.preset_flavors
        ]

        return PresetOut(
            id=preset.id,
            name=preset.name,
            category=preset.category,
            price=0,
            description=preset.description,
            hex_color=preset.hex_color,
            liquid_id=preset.liquid_id,
            bowl_id=preset.bowl_id,
            is_available=self._is_available(preset),
            liquid_name=preset.liquid.name if preset.liquid else None,
            liquid_available=getattr(preset.liquid, 'is_available', None) if preset.liquid else None,
            bowl_name=preset.bowl.name if preset.bowl else None,
            bowl_available=getattr(preset.bowl, 'is_available', None) if preset.bowl else None,
            flavors=flavors
        )