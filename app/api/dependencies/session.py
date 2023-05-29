import typing

from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from app.database.database import async_db


async def get_async_session() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    async with async_db.get_session() as session:
        yield session
