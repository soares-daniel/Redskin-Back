import fastapi


async def http_500_exc_internal_server_error() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal Server Error",
    )
