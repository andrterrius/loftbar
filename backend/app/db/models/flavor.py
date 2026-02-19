import uuid as uuid_pkg

from dataclasses import asdict

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.models import Base
from app.db.models.mixins import TimestampMixin


class DBFlavor(TimestampMixin, Base):
    __tablename__ = "flavors"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    brand: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    hex_color: Mapped[str] = mapped_column(String(32), nullable=True)