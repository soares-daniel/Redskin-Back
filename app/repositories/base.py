import fastapi
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession, AsyncSession

from app.database.database import async_db


async def get_db() -> AsyncSession:
    async with async_db.get_session() as session:
        yield session


class BaseRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession = fastapi.Depends(get_db)) -> None:
        self.async_session = async_session
