from typing import Protocol, Type

from app.db.uow import BaseUnitOfWork

class BaseTestService(Protocol):
    async def get_count_users(self, uow: BaseUnitOfWork) -> int:
        ...