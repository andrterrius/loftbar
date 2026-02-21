from typing import Protocol

from app.db.repositories.users import UsersRepository

class BaseUnitOfWork(Protocol):
    users: UsersRepository

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