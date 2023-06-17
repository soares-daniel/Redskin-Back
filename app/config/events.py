import typing

import fastapi
from loguru import logger

from app.database.events import init_db_connection, close_db_connection


def startup_handler(app: fastapi.FastAPI) -> typing.Any:
    async def startup() -> None:
        await init_db_connection(app=app)

    return startup


def shutdown_handler(app: fastapi.FastAPI) -> typing.Any:
    @logger.catch
    async def shutdown() -> None:
        await close_db_connection(app=app)

    return shutdown
