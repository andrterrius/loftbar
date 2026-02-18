from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Query, Form, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute
