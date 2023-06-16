import fastapi

from app.utilities.messages.exc_details import (
    http_404_id_details,
    http_404_username_details,
)


async def http_404_exc_id_not_found_request(_id: int) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(_id=_id),
    )


async def http_404_exc_username_not_found_request(username: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_username_details(username=username),
    )
