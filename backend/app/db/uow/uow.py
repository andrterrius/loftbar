from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.db.repositories import (
    UsersRepository,
    PresetsRepository,
    FlavorsRepository,
    FlavorCategoriesRepository,
    BowlsRepository,
    LiquidsRepository,
    TablesRepository,
    OrdersRepository,
    OrderCounterRepository,
    SettingsRepository
)


from app.db.uow import BaseUnitOfWork

class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession], auto_commit: bool = True):
        self.session_maker = session_maker
        self.auto_commit = auto_commit
        self.session: Optional[AsyncSession] = None

    async def __aenter__(self):
        self.session = self.session_maker()
        self.users = UsersRepository(self.session)
        self.flavors = FlavorsRepository(self.session)
        self.flavor_categories = FlavorCategoriesRepository(self.session)
        self.presets = PresetsRepository(self.session)
        self.bowls = BowlsRepository(self.session)
        self.liquids = LiquidsRepository(self.session)
        self.tables = TablesRepository(self.session)
        self.orders = OrdersRepository(self.session)
        self.orders_counter = OrderCounterRepository(self.session)
        self.settings = SettingsRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None and self.auto_commit:
                await self.commit()
            elif exc_type is not None:
                await self.rollback()
        except Exception as e:
            await self.rollback()
            raise
        finally:
            self._in_transaction = False
            await self.close()

    async def commit(self):
        if self.session:
            try:
                await self.session.commit()
            except SQLAlchemyError as e:
                await self.rollback()
                raise

    async def rollback(self):
        if self.session:
            try:
                await self.session.rollback()
            except SQLAlchemyError as e:
                raise

    async def flush(self):
        if self.session:
            await self.session.flush()

    async def close(self):
        if self.session:
            await self.session.close()