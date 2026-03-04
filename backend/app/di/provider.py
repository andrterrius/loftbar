from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.sql.annotation import Annotated

from app.services import (
    FlavorService,
    PresetService,
    BowlService,
    LiquidService,
    OrderService
)
from app.services.abc import (
    BaseFlavorService,
    BasePresetService,
    BaseBowlService,
    BaseLiquidService,
    BaseOrderService
)
from app.db.session_maker import new_session_maker

from app.db.uow import BaseUnitOfWork, UnitOfWork

from app.core.config import Config

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sqladmin import Admin
from app.admin import get_admin_app

class MainProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres.build_dsn())

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST, provides=BaseUnitOfWork)
    def get_uow(self, session_maker: async_sessionmaker[AsyncSession]) -> BaseUnitOfWork:
        return UnitOfWork(session_maker)

    @provide(scope=Scope.REQUEST, provides=BaseFlavorService)
    def get_flavor_service(self) -> FlavorService:
        return FlavorService()

    @provide(scope=Scope.REQUEST, provides=BaseBowlService)
    def get_bowl_service(self) -> BowlService:
        return BowlService()

    @provide(scope=Scope.REQUEST, provides=BaseLiquidService)
    def get_liquid_service(self) -> LiquidService:
        return LiquidService()

    @provide(scope=Scope.REQUEST, provides=BasePresetService)
    def get_preset_service(self) -> PresetService:
        return PresetService()

    @provide(scope=Scope.REQUEST, provides=BaseOrderService)
    def get_order_service(self) -> OrderService:
        return OrderService()