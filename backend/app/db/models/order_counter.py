from sqlalchemy import Column, Integer, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from app.db.models.mixins import TimestampMixin
from app.db.models.base import Base


class DBOrderDailyCounter(TimestampMixin, Base):
    __tablename__ = "order_daily_counter"

    counter_date: Mapped[date] = mapped_column(
        Date,
        primary_key=True,
    )

    last_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )


    def __repr__(self):
        return f"<OrderDailyCounter(date={self.counter_date}, last={self.last_number})>"