import fastapi

from app.utilities.messages.exc_details import (
    http_400_signup_credentials_details,
    http_400_signin_credentials_details,
    http_400_username_details,
    http_400_email_details,
)


async def http_exc_400_credentials_bad_signup_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_signup_credentials_details(),
    )


async def http_exc_400_credentials_bad_signin_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_signin_credentials_details(),
    )


async def http_400_exc_bad_username_request(username: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_username_details(username=username),
    )


# If needed
async def http_400_exc_bad_email_request(email: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_email_details(email=email),
    )
