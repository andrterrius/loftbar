import uuid as uuid_pkg

from typing import List

from sqlalchemy import text
from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin


class DBLiquid(TimestampMixin, Base):
    __tablename__ = "liquids"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(64), nullable=True)
    hex_color: Mapped[str] = mapped_column(String(32), nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)

    presets: Mapped[List["DBPreset"]] = relationship(
        "DBPreset",
        back_populates="liquid",
        cascade="save-update"
    )