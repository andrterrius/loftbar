from uuid import UUID

from app.db.uow import BaseUnitOfWork
from app.schemas.order import OrderCreate, OrderStatus, OrderOut
from app.schemas.preset import PresetCreate, FlavorInPreset
from app.db.models import DBOrder
from app.exceptions.order import (
    FlavorNotFoundException,
    BowlNotFoundException,
    LiquidNotFoundException,
    TableNotFoundException,
    PresetNotFoundException,
    PresetUnavailableException,
    OrderCreateException
)

from .abc import BasePresetService, BaseOrderService


class OrderService(BaseOrderService):
    async def create_order(self, uow: BaseUnitOfWork, order: OrderCreate, preset_service: BasePresetService, user_id: UUID) -> OrderOut:
        async with uow:
            table = await uow.tables.get_by_id(order.table_id)
            if not table:
                raise TableNotFoundException(order.table_id)

            preset = None
            composition_snapshot = {}
            total_price = 0.0
            is_custom = False
            custom_name = None

            if order.preset_id:
                preset = await preset_service.get_by_id_(uow, order.preset_id)
                if not preset:
                    raise PresetNotFoundException(order.preset_id)

                if not preset.is_available:
                    raise PresetUnavailableException(preset.name)

                composition_snapshot = {
                    "preset_id": str(preset.id),
                    "name": preset.name,
                    "description": preset.description,
                    "total_price": preset.price,
                    "preset_flavors": [
                        flavor.model_dump(mode='json') for flavor in preset.flavors
                    ],
                }
                total_price = preset.price

            elif order.preset:
                liquid = await uow.liquids.get_by_id(order.preset.liquid_id)
                if not liquid:
                    raise LiquidNotFoundException(order.preset.liquid_id)

                bowl = await uow.bowls.get_by_id(order.preset.bowl_id)
                if not bowl:
                    raise BowlNotFoundException(order.preset.bowl_id)

                if order.preset.flavors:
                    flavor_ids = [f.flavor_id for f in order.preset.flavors]
                    flavors = await uow.flavors.get_by_ids(flavor_ids)

                    found_flavor_ids = {f.id for f in flavors}

                    for flavor_in_preset in order.preset.flavors:
                        if flavor_in_preset.flavor_id not in found_flavor_ids:
                            raise FlavorNotFoundException(flavor_in_preset.flavor_id)

                is_custom = True

                converted_preset = PresetCreate(
                    name=f"Кастомный пресет",
                    category="Пользовательский",
                    is_available=False,
                    liquid_id=order.preset.liquid_id,
                    bowl_id=order.preset.bowl_id,
                    flavors=order.preset.flavors
                )

                preset = await preset_service.create_(uow, converted_preset, user_id)

                composition_snapshot = {
                    "preset_id": str(preset.id),
                    "name": preset.name,
                    "description": preset.description,
                    "total_price": preset.price,
                    "preset_flavors": preset.flavors,
                    "is_custom": True,
                }
                total_price = preset.price

            order = DBOrder(
                user_id=user_id,
                table_id=order.table_id,
                preset_id=preset.id if preset else None,
                status=OrderStatus.PENDING,
                total_price=total_price,
                special_requests=order.special_requests,
                is_custom=is_custom,
                custom_name=custom_name,
                composition_snapshot=composition_snapshot,
                admin_notification_sent=False,
            )

            created_order = await uow.orders.create(order)

            return OrderOut.model_validate(created_order)