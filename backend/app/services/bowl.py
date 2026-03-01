from typing import Sequence
from app.db.uow import BaseUnitOfWork
from app.schemas.bowl import BowlOut

from app.services.abc import BaseBowlService


class BowlService(BaseBowlService):
    async def get_all(self, uow: BaseUnitOfWork) -> Sequence[BowlOut]:
        async with uow:
            bowls = await uow.bowls.get_all()
            return [BowlOut.model_validate(f) for f in bowls]

    async def get_available(self, uow: BaseUnitOfWork) -> Sequence[BowlOut]:
        async with uow:
            bowls = await uow.bowls.get_available()
            return [BowlOut.model_validate(f) for f in bowls]