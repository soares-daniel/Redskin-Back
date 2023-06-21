import fastapi

from app.api.dependencies.repository import get_repository
from app.models.schemas.user import UserInResponse, UserWithToken, UserInLogin
from app.repositories.user import UserRepository
from app.security.authorization.jwt_generator import jwt_generator
from app.utilities.exceptions.http.exc_400 import http_exc_400_credentials_bad_signin_request

router = fastapi.APIRouter(prefix="/authorization", tags=["authorization"])


@router.post(
    path="/login",
    name="auth:signin",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def login(
    user_login: UserInLogin,
    user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> UserInResponse:
    try:
        db_user = await user_repo.read_user_by_password_authentication(user_login=user_login)

    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()

    access_token = jwt_generator.generate_access_token(user=db_user)

    return UserInResponse(
        id=db_user.id,
        authorized_user=UserWithToken(
            token=access_token,
            username=db_user.username,
            email=db_user.email,  # type: ignore
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        ),
    )
