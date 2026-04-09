import uuid as uuid_pkg

from typing import List
from datetime import datetime

from sqlalchemy import text
from sqlalchemy import Integer, String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin


class DBFlavor(TimestampMixin, Base):
    __tablename__ = "flavors"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    brand: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(64), nullable=True)
    hex_color: Mapped[str] = mapped_column(String(9), nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    preset_flavors: Mapped[List["DBPresetFlavor"]] = relationship(
        back_populates="flavor"
    )

    categories: Mapped[List["DBFlavorCategory"]] = relationship(
        secondary="flavor_categories_association",
        back_populates="flavors",
        lazy="selectin"
    )

    def __str__(self) -> str:
        return self.name