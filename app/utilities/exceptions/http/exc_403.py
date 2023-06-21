import fastapi

from app.utilities.messages.exc_details import (
    http_403_forbidden_details,
    http_403_permission_denied_details,
    http_403_missing_role,
)


async def http_403_exc_forbidden_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail=http_403_forbidden_details(),
    )


async def http_403_exc_permission_denied() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail=http_403_permission_denied_details(),
    )


async def http_403_exc_missing_role() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail=http_403_missing_role(),
    )