from uuid import UUID
from typing import Optional, Sequence
from app.db.uow import BaseUnitOfWork
from app.schemas.liquid import LiquidOut

from app.services.abc import BaseLiquidService


class LiquidService(BaseLiquidService):
    async def get_all(self, uow: BaseUnitOfWork) -> Sequence[LiquidOut]:
        async with uow:
            bowls = await uow.liquids.get_all()
            return [LiquidOut.model_validate(f) for f in bowls]

    async def get_available(self, uow: BaseUnitOfWork) -> Sequence[LiquidOut]:
        async with uow:
            bowls = await uow.liquids.get_available()
            return [LiquidOut.model_validate(f) for f in bowls]