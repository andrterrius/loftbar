import uuid as uuid_pkg

from typing import Optional, List

from sqlalchemy import text
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin

class DBTable(TimestampMixin, Base):
    __tablename__ = "tables"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )

    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    seats: Mapped[int] = mapped_column(Integer, default=4, nullable=False)

    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    location: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __str__(self) -> str:
        return f"Столик #{self.number} - {self.id}"