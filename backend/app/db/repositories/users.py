
from typing import TypeVar, Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID


from app.db.models import Base, DBUser
from app.db.repositories.base import SQLAlchemyRepository


class IUsersRepository(Protocol):
    async def get(self, user_id: UUID) -> DBUser | None:
        ...
    async def get_count_users(self) -> int:
        ...
    async def save_user(self, user: DBUser) -> DBUser:
        ...

class UsersRepository(SQLAlchemyRepository[DBUser], IUsersRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBUser)

    async def get(self, user_id: UUID) -> DBUser | None:
        return await self.get_by_id(user_id)

    async def get_count_users(self) -> int:
        return await self.get_count()

    async def save_user(self, user: DBUser) -> DBUser:
        instance = await self.create(user)
        await self._session.commit()
        return instance
