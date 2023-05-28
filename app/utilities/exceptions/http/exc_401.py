import fastapi

from app.utilities.messages.exc_details import (
    http_401_unauthorized_details
)


async def http_exc_401_unauthorized_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_401_unauthorized_details(),
    )
