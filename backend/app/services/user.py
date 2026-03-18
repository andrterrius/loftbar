from app.db.uow import BaseUnitOfWork
from app.schemas.user import UserCreate, UserResponse
from app.db.models import DBUser


class UserService:
    async def get_or_create_by_telegram_id(
            self,
            uow: BaseUnitOfWork,
            telegram_data: UserCreate
    ) -> UserResponse:
        async with uow:
            user = await uow.users.get_by_telegram_id(telegram_data.telegram_id)

            if not user:
                user_instance = DBUser(
                    telegram_id=telegram_data.telegram_id,
                    first_name=telegram_data.first_name,
                    last_name=telegram_data.last_name,
                    username=telegram_data.username,
                    photo_url=telegram_data.photo_url,
                    language_code=telegram_data.language_code,
                    is_premium=telegram_data.is_premium
                )
                user = await uow.users.create(user_instance)

            return UserResponse.model_validate(user)