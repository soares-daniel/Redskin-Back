from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession


class BaseService:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session
        self.logger = logger.bind(name="stdout")
