from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Query, Form, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

main_router = APIRouter(
     prefix="/api/v1",
     route_class=DishkaRoute
)