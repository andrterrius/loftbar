from fastapi import APIRouter, Request, Form, Response, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.db.uow import BaseUnitOfWork

users_router = APIRouter(
     prefix="/users",
     tags=["users"],
     route_class=DishkaRoute
)