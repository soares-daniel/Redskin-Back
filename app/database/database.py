import typing
from contextlib import asynccontextmanager

import pydantic
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)
from sqlalchemy.pool import Pool as SQLAlchemyPool, QueuePool as SQLAlchemyQueuePool

from app.config.manager import settings


class AsyncDatabase:
    def __init__(self):
        self.postgres_uri: pydantic.PostgresDsn = pydantic.PostgresDsn(
            url=settings.DB_POSTGRES_URI,
            scheme=settings.DB_POSTGRES_SCHEMA,
        )
        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=SQLAlchemyQueuePool,
        )
        self.async_sessionmaker = sqlalchemy_async_sessionmaker(bind=self.async_engine, expire_on_commit=False)
        self.pool: SQLAlchemyPool = self.async_engine.pool

    @property
    def set_async_db_uri(self) -> str | pydantic.PostgresDsn:
        """
        Set the synchronous database driver into asynchronous with asyncpg:
            `postgresql://` => `postgresql+asyncpg://`
        """
        return (
            self.postgres_uri.replace("postgresql://", "postgresql+asyncpg://")
            if self.postgres_uri
            else self.postgres_uri
        )

    @asynccontextmanager
    async def get_session(self) -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
        session = self.async_sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async_db: AsyncDatabase = AsyncDatabase()
