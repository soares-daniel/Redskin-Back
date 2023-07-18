import sys

from loguru import logger
from app.config.manager import settings


def debug_filter(record):
    return record["extra"].get("name") == "debug"


def routes_filter(record):
    return record["extra"].get("name") == "routes"


def stdout_filter(record):
    return record["extra"].get("name") == "stdout"


def configure_logging():
    """Configure logging for the app"""
    logger.remove()
    logger.add(sys.stdout, filter=stdout_filter, colorize=True, format=settings.LOGGING_FORMAT, level="INFO", enqueue=True)
    logger.add("logs/debug_{time:YYYY-MM-DD}.log", filter=debug_filter, retention="7 days", rotation="00:00",
               level="DEBUG", format=settings.LOGGING_FORMAT, enqueue=True)
    logger.add("logs/routes_{time:YYYY-MM-DD}.log", filter=routes_filter, retention="7 days", rotation="00:00",
               level="DEBUG", format=settings.LOGGING_FORMAT, enqueue=True)

    # Show enabled logging modes
    logger.trace("Trace mode enabled.")
    logger.debug("Debug mode enabled.")
    logger.info("Logging configured.")
    logger.success("Success mode enabled.")
    logger.warning("Warning mode enabled.")
    logger.error("Error mode enabled.")
    logger.critical("Critical mode enabled.")
