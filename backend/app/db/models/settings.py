from sqlalchemy import Integer, Float, event
from sqlalchemy.orm import Session, Mapped, mapped_column

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin


class DBSettings(TimestampMixin, Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    preset_base_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    strength_added_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)