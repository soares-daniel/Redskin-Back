import fastapi

from app.api.dependencies.repository import get_repository
from app.api.dependencies.role import is_user_in_role
from app.models.schemas.user import UserInCreate, UserInResponse, UserInUpdate, UserWithToken
from app.repositories.user import UserRepository
from app.security.authorization.jwt_generator import jwt_generator
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.http.exc_400 import http_exc_400_credentials_bad_signup_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request
from app.utilities.exceptions.http.exc_500 import http_500_exc_internal_server_error

router = fastapi.APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="",
    response_model=list[UserInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_users(
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository))
) -> list[UserInResponse]:
    """Get all users"""
    db_users = await user_repo.get_users()
    db_user_list = list()
    for db_user in db_users:
        access_token = jwt_generator.generate_access_token(user=db_user)
        user = UserInResponse(
            id=db_user.id,
            authorized_user=UserWithToken(
                token=access_token,
                username=db_user.username,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
            ),
        )
        db_user_list.append(user)

    return db_user_list


@router.get(
    path="/{user_id}",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_user(
        user_id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository))
) -> UserInResponse:
    """Get user by id"""
    try:
        db_user = await user_repo.get_user_by_id(user_id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(_id=user_id)

    return UserInResponse(
        id=db_user.id,
        authorized_user=UserWithToken(
            token="",
            username=db_user.username,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        ),
    )


@router.post(
    path="",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],
)
async def create_user(
        user_create: UserInCreate,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository))
) -> UserInResponse:
    """Create user"""
    try:
        await user_repo.is_username_taken(username=user_create.username)

    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_user = await user_repo.create_user(user_create=user_create)
    access_token = jwt_generator.generate_access_token(user=new_user)

    return UserInResponse(
        id=new_user.id,
        authorized_user=UserWithToken(
            token=access_token,
            username=new_user.username,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
        )
    )


@router.put(
    path="/{user_id}",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],
)
async def update_user(
        user_id: int,
        user: UserInUpdate,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository))
) -> UserInResponse:
    """Update user"""
    try:
        db_user = await user_repo.get_user_by_id(user_id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(_id=user_id)

    if user.username is not None:
        try:
            await user_repo.is_username_taken(username=user.username)

        except EntityAlreadyExists:
            raise await http_exc_400_credentials_bad_signup_request()

    updated_user = await user_repo.update_user_by_id(user_id=user_id, user_update=user)

    if updated_user is None:
        raise await http_500_exc_internal_server_error()

    access_token = jwt_generator.generate_access_token(user=updated_user)

    return UserInResponse(
        id=updated_user.id,
        authorized_user=UserWithToken(
            token=access_token,
            username=updated_user.username,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )
    )


@router.delete(
    path="/{user_id}",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],
)
async def delete_user(
        user_id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository))
) -> UserInResponse:
    """Delete user"""
    try:
        db_user = await user_repo.delete_user_by_id(user_id=user_id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(_id=user_id)

    return UserInResponse(
        id=db_user.id,
        authorized_user=UserWithToken(
            token="",
            username=db_user.username,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        ),
    )
