from fastapi import APIRouter, Request, Form, Response, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from telegram_init_data import InitData

from app.db.uow import BaseUnitOfWork

users_router = APIRouter(
     prefix="/users",
     tags=["users"],
     route_class=DishkaRoute
)

@users_router.get("/")
async def test(
        init_data: FromDishka[InitData],
):
    return init_data