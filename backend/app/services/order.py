from uuid import UUID
from typing import Optional

from app.db.uow import BaseUnitOfWork
from app.schemas.order import OrderCreate, OrderStatus, OrderOutAdmin
from app.schemas.preset import PresetCreate, PresetOut, FlavorInPreset
from app.schemas.user import UserBase
from app.schemas.table import TableBase
from app.db.models import DBOrder
from app.exceptions.order import (
    FlavorNotFoundException,
    BowlNotFoundException,
    LiquidNotFoundException,
    TableNotFoundException,
    PresetNotFoundException,
    PresetUnavailableException,
    OrderCreateException,
    TableUnavailableException,
    OrderNotFoundException,
    OrderStatusTransitionException,
    UserNotFoundException
)

from .abc import BasePresetService, BaseOrderService


class OrderService(BaseOrderService):
    async def create_order(
            self,
            uow: BaseUnitOfWork,
            order: OrderCreate,
            preset_service: BasePresetService,
            user_id: UUID
    ) -> OrderOutAdmin:
        async with uow:
            table = await uow.tables.get_by_id(order.table_id)
            if not table:
                raise TableNotFoundException(order.table_id)
            if not table.is_available:
                raise TableUnavailableException(order.table_id)

            user = await uow.users.get_by_id(user_id)
            if not user:
                raise UserNotFoundException(user_id)

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
                    "preset_flavors": [flavor.model_dump(mode='json') for flavor in converted_preset.flavors],
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

            order_out = OrderOutAdmin(
                id=created_order.id,
                status=created_order.status,
                total_price=created_order.total_price,
                special_requests=created_order.special_requests,
                is_custom=created_order.is_custom,
                custom_name=created_order.custom_name,
                composition_snapshot=created_order.composition_snapshot,
                admin_notification_sent=created_order.admin_notification_sent,
                created_at=created_order.created_at,
                updated_at=created_order.updated_at,
                confirmed_at=created_order.confirmed_at,
                ready_at=created_order.ready_at,
                completed_at=created_order.completed_at,
                user=UserBase.model_validate(user),
                table=TableBase.model_validate(table)
            )

            if preset:
                full_preset = await preset_service.get_by_id_(uow, preset.id)
                order_out.preset = full_preset

            return order_out

    async def update_order_status(self, uow: BaseUnitOfWork, order_id: UUID,
                                  new_status: OrderStatus, user_id: Optional[UUID] = None) -> OrderOutAdmin:
        async with uow:
            order = await uow.orders.get_by_id(order_id)
            if not order:
                raise OrderNotFoundException()

            if not self._can_transition_status(order.status, new_status):
                raise OrderStatusTransitionException()

            updated_order = await uow.orders.update_status(
                order_id=order_id,
                status=new_status
            )

            updated_order.preset.price = updated_order.preset.total_price

            return OrderOutAdmin.model_validate(updated_order)

    def _can_transition_status(self, current_status: OrderStatus, new_status: OrderStatus) -> bool:
        # Словарь допустимых переходов
        allowed_transitions = {
            OrderStatus.PENDING: [
                OrderStatus.CANCELLED,
                OrderStatus.IN_PROGRESS
            ],
            OrderStatus.IN_PROGRESS: [
                OrderStatus.READY,
                OrderStatus.CANCELLED
            ],
            OrderStatus.READY: [
                OrderStatus.COMPLETED,
                OrderStatus.CANCELLED
            ],
            OrderStatus.COMPLETED: [],  # Из COMPLETED нельзя изменить статус
            OrderStatus.CANCELLED: [],  # Из CANCELLED нельзя изменить статус
        }

        return new_status in allowed_transitions.get(current_status, [])