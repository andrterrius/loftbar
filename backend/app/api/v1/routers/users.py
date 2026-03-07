from fastapi import APIRouter, Request, Form, Response, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from telegram_init_data import InitData

from app.core.security.abc_jwt_service import BaseJWTService
from app.db.uow import BaseUnitOfWork

from app.schemas.auth import SuccessAuth
from app.schemas.error import ErrorResponse
from app.services.abc import BaseTgAuthService

users_router = APIRouter(
     prefix="/users",
     tags=["users"],
     route_class=DishkaRoute
)

@users_router.post("/login",
                   response_model=SuccessAuth,
                   responses={
                       401: {"model": ErrorResponse, "description": "Ошибка авторизации. error_type=telegram_auth_error"}
                   }
)
async def login_from_telegram_init_data(
        init_data: FromDishka[InitData],
        uow: FromDishka[BaseUnitOfWork],
        jwt_service: FromDishka[BaseJWTService],
        tg_auth_service: FromDishka[BaseTgAuthService],
):
    """Обменять telegram init data на jwt токен (access_token)"""
    async with uow:
        return await tg_auth_service.authenticate(uow, jwt_service, init_data)