import json

import fastapi
from loguru import logger


routes_logger = logger.bind(name="routes")


async def logging_dependency(request: fastapi.Request):
    routes_logger.debug(f"{request.method} {request.url}")
    routes_logger.debug("Params:")
    for name, value in request.path_params.items():
        routes_logger.debug(f"\t{name}: {value}")
    routes_logger.debug("Headers:")
    for name, value in request.headers.items():
        routes_logger.debug(f"\t{name}: {value}")

    # Logging the body
    body_bytes = await request.body()
    try:
        # Try to parse JSON body for better logging readability
        body_data = json.loads(body_bytes)

        routes_logger.debug(f"Body:")
        for name, value in body_data.items():
            routes_logger.debug(f"\t{name}: {value}")
    except json.JSONDecodeError:
        # If not JSON, just log the raw body
        if not body_bytes:
            routes_logger.debug(f"Body: EMPTY")
        else:
            routes_logger.debug(f"Body (raw): {body_bytes.decode()}")
