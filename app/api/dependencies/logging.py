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
