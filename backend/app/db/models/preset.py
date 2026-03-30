import uuid as uuid_pkg

from typing import Optional, List, Tuple

from sqlalchemy import text, Boolean, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin


class DBPreset(TimestampMixin, Base):
    __tablename__ = "presets"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    strength: Mapped[float] = mapped_column(Integer, default=1, nullable=False)
    description: Mapped[str] = mapped_column(String(64), nullable=True)
    hex_color: Mapped[str] = mapped_column(String(9), nullable=True)

    preset_flavors: Mapped[List["DBPresetFlavor"]] = relationship(
        back_populates="preset",
        lazy="selectin"
    )

    liquid_id: Mapped[Optional[uuid_pkg.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("liquids.id", ondelete="SET NULL"),
        nullable=True
    )

    bowl_id: Mapped[Optional[uuid_pkg.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bowls.id", ondelete="SET NULL"),
        nullable=True
    )

    created_by_id: Mapped[Optional[uuid_pkg.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    settings_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("settings.id", ondelete="SET NULL"),
        nullable=False,
        server_default=text("1")
    )

    liquid: Mapped[Optional["DBLiquid"]] = relationship(
        "DBLiquid",
        backref="presets"
    )
    bowl: Mapped[Optional["DBBowl"]] = relationship(
        "DBBowl",
        backref="presets"
    )
    created_by: Mapped[Optional["DBUser"]] = relationship(
        "DBUser",
        back_populates="presets"
    )

    settings: Mapped[Optional["DBSettings"]] = relationship(
        "DBSettings",
        backref="presets",
        lazy="selectin"
    )

    @property
    def availability_info(self) -> Tuple[bool, Optional[str]]:
        """
        Возвращает кортеж (доступен, причина)
        Для админки и API
        """
        # Базовая проверка
        if not self.is_available:
            return False, "Пресет отключен"

        # Проверка жидкости
        if self.liquid and not self.liquid.is_available:
            return False, f"Недоступна жидкость: {self.liquid.name}"

        # Проверка чаши
        if self.bowl and not self.bowl.is_available:
            return False, f"Недоступна чаша: {self.bowl.name}"

        # Проверка вкусов
        total_percent = 0
        for pf in self.preset_flavors:
            if not pf.flavor:
                return False, f"Вкус не найден (ID: {pf.flavor_id})"
            if not pf.flavor.is_available:
                return False, f"Недоступен вкус: {pf.flavor.name}"
            total_percent += pf.percent

        # Проверка суммы процентов
        if abs(total_percent - 100) > 0.01:
            return False, f"Сумма процентов {total_percent:.1f}% (должно быть 100%)"

        return True, None

    @property
    def is_fully_available(self) -> bool:
        """Только булево значение для API"""
        return self.availability_info[0]

    @property
    def unavailability_reason(self) -> Optional[str]:
        """Причина недоступности для админки"""
        return self.availability_info[1]

    @property
    def total_price(self) -> int:
        """Расчет полной цены пресета"""
        if not self.settings:
            return 0

        total = self.settings.preset_base_price

        if self.liquid and self.liquid.is_available:
            total += self.liquid.price

        if self.bowl and self.bowl.is_available:
            total += self.bowl.price

        if self.strength >= 9:
            total += self.settings.strength_added_price


        return total

    def __str__(self) -> str:
        return self.name