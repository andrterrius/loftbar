import uuid as uuid_pkg

from typing import Optional, List

from sqlalchemy import text, ForeignKey, String, Float
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

    preset_flavors: Mapped[List["DBPresetFlavor"]] = relationship(
        back_populates="preset",
        cascade="all, delete-orphan"
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