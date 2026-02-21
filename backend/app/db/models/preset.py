import uuid as uuid_pkg

from typing import Optional, List

from sqlalchemy import text
from sqlalchemy import String, Float
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
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(64), nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)

    preset_ingredients: Mapped[List["DBPresetIngredient"]] = relationship(
        back_populates="preset",
        cascade="all, delete-orphan"
    )

    liquid: Mapped[Optional["DBLiquid"]] = relationship(
        "DBLiquid",
        back_populates="presets"
    )

    created_by: Mapped[Optional["DBUser"]] = relationship(
        "DBUser",
        back_populates="presets"
    )