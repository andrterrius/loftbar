from fastapi import APIRouter, Request, Form, Response, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.services import TestService

from app.db.uow import BaseUnitOfWork

from app.services.abc import BaseTestService

test_router = APIRouter(
     prefix="/test",
     tags=["test"],
     route_class=DishkaRoute
)

@test_router.post("/")
async def test(
        service: FromDishka[BaseTestService],
        uow: FromDishka[BaseUnitOfWork],
):
    result = await service.get_count_users(uow)
    return {"status": "ok", "result": result}