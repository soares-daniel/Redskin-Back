import typing

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from app.services.base import BaseService
from app.api.dependencies.session import get_async_session


def get_service(
    service_type: typing.Type[BaseService],
) -> typing.Callable[[SQLAlchemyAsyncSession], BaseService]:
    def _get_service(
        async_session: SQLAlchemyAsyncSession = fastapi.Depends(get_async_session),
    ) -> BaseService:
        return service_type(async_session=async_session)

    return _get_service
