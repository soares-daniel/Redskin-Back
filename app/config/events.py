from typing import Any

from loguru import logger
from fastapi import FastAPI

from app.database.events import init_db_connection, close_db_connection


def startup_handler(app: FastAPI) -> Any:
    async def startup() -> None:
        await init_db_connection(app=app)

    return startup


def shutdown_handler(app: FastAPI) -> Any:
    @logger.catch
    async def shutdown() -> None:
        await close_db_connection(app=app)

    return shutdown
