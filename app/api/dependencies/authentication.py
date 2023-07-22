from jose import JWTError
from fastapi import Depends, HTTPException, status, Request

from app.security.authorization.jwt_generator import jwt_generator
from app.models.db.user import User
from app.repositories.user import UserRepository
from app.utilities.exceptions.http.exc_401 import http_exc_401_unauthorized_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_username_not_found_request


async def get_current_user(
    request: Request,
    user_repo: UserRepository = Depends(UserRepository),
) -> User:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        username = jwt_generator.retrieve_details_from_token(token)[0]  # Retrieve username from token
    except JWTError:
        raise await http_exc_401_unauthorized_request()

    db_user = await user_repo.get_user_by_username(username)
    if db_user is None:
        raise await http_404_exc_username_not_found_request(username=username)

    return db_user
