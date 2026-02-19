from __future__ import annotations

from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base
from app.db.models.mixins import TimestampMixin


class DBUser(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(128))
    username: Mapped[str | None] = mapped_column(String(64))
    photo_url: Mapped[str] = mapped_column(String(255))
    language_code: Mapped[str | None] = mapped_column(String(10))
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)