import fastapi

from app.utilities.messages.exc_details import (
    http_401_unauthorized_details
)


async def http_exc_401_unauthorized_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail=http_401_unauthorized_details(),
    )
