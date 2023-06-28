import fastapi

from app.utilities.messages.exc_details import (
    http_404_id_details,
    http_404_username_details,
)


async def http_404_exc_event_id_not_found_request(_id: int) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(_object="event", _id=_id),
    )


async def http_404_exc_role_id_not_found_request(_id: int) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(_object="role", _id=_id),
    )


async def http_404_exc_user_id_not_found_request(_id: int) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(_object="user", _id=_id),
    )


async def http_404_exc_username_not_found_request(username: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_username_details(username=username),
    )
