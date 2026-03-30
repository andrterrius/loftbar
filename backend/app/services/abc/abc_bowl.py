from typing import Protocol, Sequence

from app.db.uow import BaseUnitOfWork
from app.schemas.bowl import BowlOut


class BaseBowlService(Protocol):
    async def get_all(self, uow: BaseUnitOfWork) -> Sequence[BowlOut]:
        ...

    async def get_available(self, uow: BaseUnitOfWork) -> Sequence[BowlOut]:
        ...
