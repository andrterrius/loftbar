from typing import Protocol, Sequence

from app.db.uow import BaseUnitOfWork
from app.schemas.liquid import LiquidOut


class BaseLiquidService(Protocol):
    async def get_all(self, uow: BaseUnitOfWork) -> Sequence[LiquidOut]:
        ...

    async def get_available(self, uow: BaseUnitOfWork) -> Sequence[LiquidOut]:
        ...
