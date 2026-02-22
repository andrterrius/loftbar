from typing import Protocol

from app.db.repositories import (
    UsersRepository,
    PresetsRepository,
    FlavorsRepository,
    BowlsRepository,
    LiquidsRepository,
)


class BaseUnitOfWork(Protocol):
    users: UsersRepository
    presets: PresetsRepository
    flavors: FlavorsRepository
    bowls: BowlsRepository
    liquids: LiquidsRepository

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