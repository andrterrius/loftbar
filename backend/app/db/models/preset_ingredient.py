import uuid as uuid_pkg
from sqlalchemy import Table, Column, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped


from app.db.models.base import Base


class DBPresetIngredient(Base):
    __tablename__ = "preset_ingredients"

    preset_id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("presets.id", ondelete="CASCADE"),
        primary_key=True
    )
    ingredient_id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        primary_key=True
    )
    percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    preset: Mapped["DBPreset"] = relationship(back_populates="preset_ingredients")
    ingredient: Mapped["DBIngredient"] = relationship(back_populates="preset_ingredients")