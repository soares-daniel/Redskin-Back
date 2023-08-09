import fastapi
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.repository import get_repository
from app.models.schemas.user import UserInResponse, UserInLogin
from app.repositories.user import UserRepository
from app.config.manager import settings
from app.security.authorization.jwt_generator import jwt_generator
from app.utilities.exceptions.http.exc_400 import http_exc_400_credentials_bad_signin_request
router = fastapi.APIRouter(prefix="/authorization", tags=["authorization"])


@router.post(
    path="/login",
    name="auth:login",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> UserInResponse:
    try:
        user_login = UserInLogin(
            username=form_data.username,
            password=form_data.password,
        )
        db_user = await user_repo.read_user_by_password_authentication(user_login=user_login)
    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()

    access_token = jwt_generator.generate_access_token(user=db_user)

    # Set the cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME,
        secure=False,  # The cookie will be set only on https if True
    )

    return UserInResponse(
        id=db_user.id,
        username=db_user.username,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


@router.post(
    path="/logout",
    name="auth:logout",
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def logout(response: Response) -> dict[str, str]:
    response.set_cookie(key="access_token", value="", httponly=True, max_age=0)

    return {"message": "Successfully logged out"}

