from enum import Enum as PyEnum
from datetime import datetime

import uuid as uuid_pkg

from typing import Optional

from sqlalchemy import text
from sqlalchemy import Integer, String, ForeignKey, Boolean, Enum, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.postgresql import JSONB

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin


class OrderStatus(str, PyEnum):
    PENDING = "pending"        # Ожидает подтверждения/приготовления
    IN_PROGRESS = "in_progress" # Готовится (админ подтвердил)
    READY = "ready"            # Готов (уведомление админу отправлено)
    COMPLETED = "completed"     # Завершен (оплачен/получен)
    CANCELLED = "cancelled"     # Отменен


class DBOrder(TimestampMixin, Base):
    __tablename__ = "orders"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )

    daily_number: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    user_id: Mapped[Optional[uuid_pkg.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    table_id: Mapped[Optional[uuid_pkg.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tables.id", ondelete="SET NULL"),
        nullable=True
    )

    preset_id: Mapped[Optional[uuid_pkg.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("presets.id", ondelete="SET NULL"),
        nullable=True
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status", create_type=True),
        default=OrderStatus.PENDING,
        nullable=False
    )

    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    special_requests: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    is_custom: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    custom_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    composition_snapshot: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ready_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    admin_notification_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped[Optional["DBUser"]] = relationship("DBUser", back_populates="orders")
    table: Mapped[Optional["DBTable"]] = relationship("DBTable", backref="orders")
    preset: Mapped[Optional["DBPreset"]] = relationship("DBPreset")

    def __str__(self) -> str:
        order_type = "Кастомный" if self.is_custom else "Готовый"
        return f"Заказ {order_type} #{self.id} - {self.status.value}"