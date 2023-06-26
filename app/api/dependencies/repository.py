import typing

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from app.api.dependencies.session import get_async_session
from app.repositories.base import BaseRepository


def get_repository(repo_type: typing.Type[BaseRepository]):
    def _get_repo(async_session: SQLAlchemyAsyncSession = fastapi.Depends(get_async_session)) -> BaseRepository:
        return repo_type(async_session=async_session)
    return _get_repo
