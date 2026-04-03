import uuid as uuid_pkg
from typing import List

from sqlalchemy import text, ForeignKey, UniqueConstraint
from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin

class DBFlavorCategoryAssociation(Base):
    __tablename__ = "flavor_categories_association"

    flavor_id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("flavors.id", ondelete="CASCADE"),
        primary_key=True
    )
    category_id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("flavor_categories.id", ondelete="CASCADE"),
        primary_key=True
    )

    def __str__(self) -> str:
        return f"Категория"


class DBFlavorCategory(TimestampMixin, Base):
    __tablename__ = "flavor_categories"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    flavors: Mapped[List["DBFlavor"]] = relationship(
        secondary="flavor_categories_association",
        back_populates="categories",
        lazy="selectin"
    )

    def __str__(self) -> str:
        return self.name