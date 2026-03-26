# app/repositories/order_counter.py
from typing import Protocol, Optional, Any, Sequence
from datetime import date, datetime, timedelta
from sqlalchemy import select, update, delete, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import DBOrderDailyCounter
from app.core.common import utcnow
from .base import SQLAlchemyRepository


class IOrderCounterRepository(Protocol):
    """Интерфейс репозитория счетчиков заказов"""

    async def get_next_number(self, order_date: date) -> int:
        """
        Получить следующий номер заказа для указанной даты.
        Атомарно увеличивает счетчик и возвращает новое значение.
        """
        ...

    async def get_current_number(self, order_date: date) -> int:
        """
        Получить текущий номер для даты (без инкремента).
        Возвращает 0, если счетчик не существует.
        """
        ...

    async def get_by_date(self, order_date: date) -> Optional[DBOrderDailyCounter]:
        """Получить счетчик по дате"""
        ...

    async def delete_counter(self, order_date: date) -> bool:
        """Удалить счетчик для указанной даты"""
        ...

    async def set_counter(self, order_date: date, last_number: int) -> DBOrderDailyCounter:
        """Установить счетчик для даты (принудительно)"""
        ...


class OrderCounterRepository(SQLAlchemyRepository[DBOrderDailyCounter]):
    """Репозиторий для работы со счетчиками заказов"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, DBOrderDailyCounter)

    async def get_next_number(self, order_date: date) -> int:
        stmt = insert(DBOrderDailyCounter).values(
            counter_date=order_date,
            last_number=1,
        ).on_conflict_do_update(
            index_elements=['counter_date'],
            set_={
                'last_number': DBOrderDailyCounter.last_number + 1,
            }
        ).returning(DBOrderDailyCounter.last_number)

        result = await self._session.execute(stmt)
        next_number = result.scalar_one()

        await self._session.flush()
        return next_number

    async def get_current_number(self, order_date: date) -> int:
        """Получить текущий номер для даты (без инкремента)"""
        stmt = select(DBOrderDailyCounter.last_number).where(
            DBOrderDailyCounter.counter_date == order_date
        )
        result = await self._session.execute(stmt)
        current = result.scalar_one_or_none()
        return current or 0

    async def get_by_date(self, order_date: date) -> Optional[DBOrderDailyCounter]:
        """Получить счетчик по дате"""
        stmt = select(DBOrderDailyCounter).where(
            DBOrderDailyCounter.counter_date == order_date
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_counter(self, order_date: date) -> bool:
        """Удалить счетчик для указанной даты"""
        stmt = delete(DBOrderDailyCounter).where(
            DBOrderDailyCounter.counter_date == order_date
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.rowcount > 0

    async def set_counter(self, order_date: date, last_number: int) -> DBOrderDailyCounter:
        """
        Установить счетчик для даты (принудительно).
        Используется для исправления ошибок или ручного вмешательства.
        """
        stmt = insert(DBOrderDailyCounter).values(
            counter_date=order_date,
            last_number=last_number,
            updated_at=utcnow()
        ).on_conflict_do_update(
            index_elements=['counter_date'],
            set_={
                'last_number': last_number,
                'updated_at': utcnow()
            }
        ).returning(DBOrderDailyCounter)

        result = await self._session.execute(stmt)
        counter = result.scalar_one()
        await self._session.flush()
        return counter
