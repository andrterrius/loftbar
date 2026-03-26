from typing import Protocol

from app.db.repositories import (
    UsersRepository,
    PresetsRepository,
    FlavorsRepository,
    BowlsRepository,
    LiquidsRepository,
    TablesRepository,
    OrdersRepository,
    OrderCounterRepository,
    SettingsRepository
)


class BaseUnitOfWork(Protocol):
    users: UsersRepository
    presets: PresetsRepository
    flavors: FlavorsRepository
    bowls: BowlsRepository
    liquids: LiquidsRepository
    tables: TablesRepository
    orders: OrdersRepository
    orders_counter: OrderCounterRepository
    settings: SettingsRepository
    settings: SettingsRepository

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def flush(self):
        ...

    async def close(self):
        ...