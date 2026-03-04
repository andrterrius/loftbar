from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from app.schemas.error import ErrorResponse

from app.exceptions.base import BaseServiceException


async def base_service_exception_handler(request: Request, exc: BaseServiceException):
    """
    Обработчик для сервисных ошибок
    """
    error_response = ErrorResponse(
        success=False,
        message=exc.message,
        error_type="server_error",

    )

    if exc.details:
        error_response.details = exc.details

    if hasattr(exc, 'field') and exc.field:
        error_response.field = exc.field
    status_code = status.HTTP_400_BAD_REQUEST
    if hasattr(exc, 'status_code'):
        status_code = exc.status_code

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(error_response)
    )