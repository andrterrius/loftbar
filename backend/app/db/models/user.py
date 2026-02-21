import uuid as uuid_pkg

from typing import List

from sqlalchemy import text

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base
from app.db.models.mixins import TimestampMixin


class DBUser(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    username: Mapped[str] = mapped_column(String(64), nullable=True)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    presets: Mapped[List["DBPreset"]] = relationship(
        "DBPreset",
        back_populates="created_by",
        cascade="all, delete-orphan"
    )