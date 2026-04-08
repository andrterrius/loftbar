from typing import Sequence
from app.db.uow import BaseUnitOfWork
from app.schemas.bowl import BowlOut
from app.services.abc import BaseBowlService

from app.core.common import its_evening_now

class BowlService(BaseBowlService):

    def _format_bowls(self, bowls: Sequence) -> Sequence[BowlOut]:
        is_evening_price = its_evening_now()
        bowls_out = []
        for bowl in bowls:
            bowl_model = BowlOut.model_validate(bowl)
            if is_evening_price:
                bowl_model.added_price = bowl.added_price_evening
            bowls_out.append(bowl_model)
        return bowls_out

    async def get_all(self, uow: BaseUnitOfWork) -> Sequence[BowlOut]:
        async with uow:
            bowls = await uow.bowls.get_all()
            return self._format_bowls(bowls)

    async def get_available(self, uow: BaseUnitOfWork) -> Sequence[BowlOut]:
        async with uow:
            bowls = await uow.bowls.get_available()
            return self._format_bowls(bowls)