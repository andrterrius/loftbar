from uuid import UUID
from typing import Protocol, Optional, Sequence, Any, List
from sqlalchemy import select, func, delete, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.db.models import DBUser


class IUsersRepository(Protocol):

    async def get_by_id(self, _id: UUID) -> Optional[Any]:
        ...

    async def get_one(self, **filters: Any) -> Optional[Any]:
        ...

    async def get_all(self, order_by: Any = None, **filters: Any) -> Sequence[Any]:
        ...

    async def get_count(self, **filters: Any) -> int:
        ...

    async def create(self, instance: Any) -> Any:
        ...

    async def update(self, instance: Any) -> Any:
        ...

    async def delete(self, _id: UUID) -> None:
        ...

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[Any]:
        ...

    async def get_by_username(self, username: str) -> Optional[Any]:
        ...

    async def get_admins(self) -> Sequence[Any]:
        ...

    async def get_premium_users(self) -> Sequence[Any]:
        ...

    async def get_users_with_presets(self) -> Sequence[Any]:
        ...

    async def get_count_admins(self) -> int:
        ...

    async def get_count_premium(self) -> int:
        ...

    async def update_user_profile(
            self,
            user_id: UUID,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            username: Optional[str] = None,
            photo_url: Optional[str] = None,
            language_code: Optional[str] = None
    ) -> Optional[Any]:
        ...

    async def set_admin_status(self, user_id: UUID, is_admin: bool) -> Optional[Any]:
        ...

    async def get_or_create_by_telegram_id(
            self,
            telegram_id: int,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            username: Optional[str] = None,
            photo_url: Optional[str] = None,
            language_code: Optional[str] = None,
            is_premium: bool = False
    ) -> Any:
        ...


class UsersRepository(SQLAlchemyRepository[DBUser], IUsersRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DBUser)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[DBUser]:
        return await self.get_one(telegram_id=telegram_id)

    async def get_by_username(self, username: str) -> Optional[DBUser]:
        return await self.get_one(username=username)

    async def get_admins(self) -> Sequence[DBUser]:
        return await self.get_all(is_admin=True)

    async def get_premium_users(self) -> Sequence[DBUser]:
        return await self.get_all(is_premium=True)

    async def get_users_with_presets(self) -> Sequence[DBUser]:
        stmt = select(DBUser).where(DBUser.presets.any())
        return (await self._session.scalars(stmt)).all()

    async def get_count_admins(self) -> int:
        return await self.get_count(is_admin=True)

    async def get_count_premium(self) -> int:
        return await self.get_count(is_premium=True)

    async def update_user_profile(
            self,
            user_id: UUID,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            username: Optional[str] = None,
            photo_url: Optional[str] = None,
            language_code: Optional[str] = None
    ) -> Optional[DBUser]:
        user = await self.get_by_id(user_id)
        if user:
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if username is not None:
                user.username = username
            if photo_url is not None:
                user.photo_url = photo_url
            if language_code is not None:
                user.language_code = language_code
            return await self.update(user)
        return None

    async def set_admin_status(self, user_id: UUID, is_admin: bool) -> Optional[DBUser]:
        user = await self.get_by_id(user_id)
        if user:
            user.is_admin = is_admin
            return await self.update(user)
        return None

    async def get_or_create_by_telegram_id(
            self,
            telegram_id: int,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            username: Optional[str] = None,
            photo_url: Optional[str] = None,
            language_code: Optional[str] = None,
            is_premium: bool = False
    ) -> DBUser:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user

        user = DBUser(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            photo_url=photo_url,
            language_code=language_code,
            is_premium=is_premium
        )
        return await self.create(user)