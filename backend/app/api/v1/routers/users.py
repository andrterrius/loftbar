from fastapi import APIRouter, Request, Form, Response, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from telegram_init_data import InitData

from app.core.security.abc_jwt_service import BaseJWTService
from app.db.uow import BaseUnitOfWork

from app.schemas.auth import SuccessAuth

users_router = APIRouter(
     prefix="/users",
     tags=["users"],
     route_class=DishkaRoute
)

@users_router.post("/login",
                   response_model=SuccessAuth)
async def login_from_telegram_init_data(
        # init_data: FromDishka[InitData],
        uow: FromDishka[BaseUnitOfWork],
        jwt_service: FromDishka[BaseJWTService]
):
    async with uow:
        #заглушка)))
        user_id = await uow.users.get_one()
        return SuccessAuth(access_token=jwt_service.create_access_token(user_id.id))