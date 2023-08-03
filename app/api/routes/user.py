import fastapi

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.repository import get_repository
from app.api.dependencies.role import is_user_in_role
from app.api.dependencies.service import get_service
from app.models.db.user import User
from app.models.schemas.event_operation import EventOperation
from app.models.schemas.event_type import EventTypeInResponse
from app.models.schemas.role import RoleInResponse
from app.models.schemas.user import UserInCreate, UserInResponse, UserInUpdate
from app.models.schemas.user_role import UserRoleInAssign, UserRoleInRemove
from app.repositories.role_event_type import RoleEventTypeRepository
from app.repositories.user import UserRepository
from app.services.notification import NotificationService
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.http.exc_500 import http_500_exc_internal_server_error
from app.utilities.exceptions.http.exc_400 import http_400_exc_bad_username_request
from app.utilities.exceptions.http.exc_404 import (http_404_exc_user_id_not_found_request,
                                                   http_404_exc_user_role_not_found_request,
                                                   http_404_exc_user_role_relation_not_found_request)

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
        user = UserInResponse(
            id=db_user.id,
            username=db_user.username,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            profile_pic_url=db_user.profile_pic_url,
        )
        db_user_list.append(user)

    return db_user_list


@router.get(
    path="/user/{user_id}",
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
        raise await http_404_exc_user_id_not_found_request(_id=user_id)

    return UserInResponse(
        id=db_user.id,
        username=db_user.username,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        profile_pic_url=db_user.profile_pic_url,
    )


@router.post(
    path="/create",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],

)
async def create_user(
        user_create: UserInCreate,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> UserInResponse:
    """Create user"""
    try:
        await user_repo.is_username_taken(username=user_create.username)

    except EntityAlreadyExists:
        raise await http_400_exc_bad_username_request(username=user_create.username)

    try:
        new_user = await user_repo.create_user(user_create=user_create)
    except ValueError as e:
        raise await http_500_exc_internal_server_error(message=e.args[0])

    response = UserInResponse(
        id=new_user.id,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
        profile_pic_url=new_user.profile_pic_url,
    )

    await notif_service.send_user_notification(user=response, event_operation=EventOperation.USER_CREATE)

    return response


@router.put(
    path="/update/{user_id}",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],
)
async def update_user(
        user_id: int,
        user: UserInUpdate,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> UserInResponse:
    """Update user"""
    try:
        await user_repo.get_user_by_id(user_id)
    except EntityDoesNotExist:
        raise await http_404_exc_user_id_not_found_request(_id=user_id)

    if user.username is not None:
        try:
            await user_repo.is_username_taken(username=user.username)

        except EntityAlreadyExists:
            raise await http_400_exc_bad_username_request(username=user.username)

    updated_user = await user_repo.update_user_by_id(user_id=user_id, user_update=user)

    if updated_user is None:
        raise await http_500_exc_internal_server_error()

    response = UserInResponse(
        id=updated_user.id,
        username=updated_user.username,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
        profile_pic_url=updated_user.profile_pic_url,
    )

    await notif_service.send_user_notification(user=response, event_operation=EventOperation.USER_UPDATE)

    return response


@router.delete(
    path="/delete/{user_id}",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],
)
async def delete_user(
        user_id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> UserInResponse:
    """Delete user"""
    try:
        db_user = await user_repo.delete_user_by_id(user_id=user_id)

    except EntityDoesNotExist:
        raise await http_404_exc_user_id_not_found_request(_id=user_id)

    response = UserInResponse(
        id=db_user.id,
        username=db_user.username,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        profile_pic_url=db_user.profile_pic_url,
    )

    await notif_service.send_user_notification(user=response, event_operation=EventOperation.USER_DELETE)

    return response


@router.get(
    path="/user/{user_id}/roles",
    response_model=list[RoleInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_user_roles(
        user_id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository))
) -> list[RoleInResponse]:
    """Get user roles"""
    try:
        db_user = await user_repo.get_user_by_id(user_id)

    except EntityDoesNotExist:
        raise await http_404_exc_user_id_not_found_request(_id=user_id)

    db_roles = await user_repo.get_roles_for_user(user_id=db_user.id)  # type: ignore
    db_role_list = list()
    for db_role in db_roles:
        role = RoleInResponse(
            id=db_role.id,
            name=db_role.name
        )
        db_role_list.append(role)

    return db_role_list


@router.post(
    path="/user/{user_id}/assign/{role_id}",
    response_model=UserRoleInAssign,
    status_code=fastapi.status.HTTP_201_CREATED,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],
)
async def assign_role_to_user(
        user_id: int,
        role_id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> UserRoleInAssign:
    """Assign role to user"""
    try:
        user_role = await user_repo.assign_role_to_user(user_id=user_id, role_id=role_id)

    except EntityDoesNotExist:
        raise await http_404_exc_user_role_not_found_request(user_id=user_id, role_id=role_id)

    await notif_service.send_user_role_notification(
        user_role=user_role,
        event_operation=EventOperation.USER_ROLE_ASSIGN
    )

    return user_role


@router.delete(
    path="/user/{user_id}/remove/{role_id}",
    response_model=UserRoleInRemove,
    status_code=fastapi.status.HTTP_200_OK,
)
async def remove_role_from_user(
        user_id: int,
        role_id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> UserRoleInRemove:
    """Remove role from user"""
    try:
        user_role = await user_repo.remove_role_from_user(user_id=user_id, role_id=role_id)

    except EntityDoesNotExist:
        raise await http_404_exc_user_role_relation_not_found_request(user_id=user_id, role_id=role_id)

    await notif_service.send_user_role_notification(
        user_role=user_role,
        event_operation=EventOperation.USER_ROLE_REMOVE
    )

    return user_role


@router.get(
    path="/event_types",
    response_model=list[EventTypeInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_event_types_for_user(
        current_user: User = fastapi.Depends(get_current_user),
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        role_event_type_repo: RoleEventTypeRepository = fastapi.Depends(
            get_repository(repo_type=RoleEventTypeRepository)),
) -> list[EventTypeInResponse]:
    """Get event types for user"""
    try:
        roles = await user_repo.get_roles_for_user(user_id=current_user.id)  # type: ignore

    except EntityDoesNotExist:
        return []

    event_types_list = []
    for role in roles:
        event_types = await role_event_type_repo.get_event_types_for_role(role_id=role.id)  # type: ignore
        for event_type in event_types:
            event_types_list.append(event_type)

    # Remove duplicates
    event_types_list = list(dict.fromkeys(event_types_list))

    return [EventTypeInResponse.from_orm(event_type) for event_type in event_types_list]
