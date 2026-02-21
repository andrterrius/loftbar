
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DBUser
from app.db.repositories.users import UsersRepository
from app.db.uow import BaseUnitOfWork


class TestService:
    def __init__(self):
        self.test = "F"
    async def get_count_users(self, uow: BaseUnitOfWork) -> int:
        async with uow:
            return await uow.users.get_count()