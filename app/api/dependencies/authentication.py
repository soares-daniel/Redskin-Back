import jose
import fastapi
from fastapi.security import OAuth2PasswordBearer

from app.security.authorization.jwt_generator import jwt_generator
from app.models.db.user import User
from app.repositories.user import UserRepository
from app.config.manager import settings
from app.utilities.exceptions.http.exc_401 import http_exc_401_unauthorized_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_username_not_found_request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/authorization/login")


async def get_current_user(
        token: str = fastapi.Depends(oauth2_scheme),
        user_repo: UserRepository = fastapi.Depends(UserRepository)
) -> User:
    try:
        username = jwt_generator.retrieve_details_from_token(token)[0]  # Retrieve username from token
    except jose.JWTError:
        raise await http_exc_401_unauthorized_request()

    db_user = await user_repo.get_user_by_username(username)
    if db_user is None:
        raise await http_404_exc_username_not_found_request(username=username)

    return db_user
