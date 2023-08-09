import fastapi

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.repository import get_repository
from app.api.dependencies.role import is_user_in_role
from app.api.dependencies.service import get_service
from app.models.db.user import User
from app.models.schemas.event_operation import EventOperation
from app.models.schemas.role import RoleInResponse, RoleInUpdate, RoleInCreate
from app.models.schemas.role_event_type import RoleEventTypeInResponse, RoleEventTypeInCreate
from app.models.schemas.user import UserInResponse, UserInUpdate, UserInCreate
from app.models.schemas.user_role import UserRoleInAssign, UserRoleInRemove
from app.repositories.role import RoleRepository
from app.repositories.role_event_type import RoleEventTypeRepository
from app.repositories.user import UserRepository
from app.services.notification import NotificationService
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.http.exc_400 import http_400_exc_bad_username_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_user_id_not_found_request, \
    http_404_exc_user_role_not_found_request, http_404_exc_user_role_relation_not_found_request
from app.utilities.exceptions.http.exc_500 import http_500_exc_internal_server_error

router = fastapi.APIRouter(prefix="/admin", tags=["admin"], dependencies=[fastapi.Depends(is_user_in_role(role="admin"))])


@router.get(
    path="/users",
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
    path="/roles/{user_id}",
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
    path="/create/user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
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
    path="/update/user/{user_id}",
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
    path="/delete/user/{user_id}",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_user(
        user_id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> UserInResponse:
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


@router.post(
    path="/user/{user_id}/assign/role/{role_id}",
    response_model=UserRoleInAssign,
    status_code=fastapi.status.HTTP_201_CREATED,
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


@router.post(
    path="/user/{user_id}/remove/role/{role_id}",
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


@router.post(
    path="/roles/create",
    response_model=RoleInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_role(
        role_create: RoleInCreate,
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> RoleInResponse:
    """Create new role"""

    created_role = await role_repo.create_role(role_create=role_create)

    response = RoleInResponse.from_orm(created_role)

    await notif_service.send_role_notification(role=response, event_operation=EventOperation.ROLE_CREATE)

    return response


@router.put(
    path="/roles/update/{role_id}",
    response_model=RoleInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_role(
        role_id: int,
        role_update: RoleInUpdate,
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> RoleInResponse:
    """Update role"""
    try:
        await role_repo.get_role_by_id(role_id)
    except EntityDoesNotExist:
        raise await http_404_exc_user_id_not_found_request(_id=role_id)

    updated_role = await role_repo.update_role_by_id(role_id=role_id, role_update=role_update)

    if updated_role is None:
        raise await http_500_exc_internal_server_error()

    response = RoleInResponse.from_orm(updated_role)

    await notif_service.send_role_notification(role=response, event_operation=EventOperation.ROLE_UPDATE)

    return response


@router.delete(
    path="/roles/delete/{role_id}",
    response_model=RoleInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_role(
        role_id: int,
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> RoleInResponse:
    """Delete role"""

    deleted_role = await role_repo.delete_role_by_id(role_id)

    if deleted_role is None:
        raise fastapi.HTTPException(status_code=404, detail="Role not found")

    response = RoleInResponse.from_orm(deleted_role)

    await notif_service.send_role_notification(role=response, event_operation=EventOperation.ROLE_DELETE)

    return response


@router.post(
    path="/roles/{role_id}/permissions",
    response_model=RoleEventTypeInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
    dependencies=[fastapi.Depends(is_user_in_role(role="admin"))],
)
async def create_permission(
        role_event_type_create: RoleEventTypeInCreate,
        role_event_type_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))

) -> RoleEventTypeInResponse:
    """Create new permission"""

    created_permission = await role_event_type_repo.create_permissions(permission_create=role_event_type_create)

    response = RoleEventTypeInResponse.from_orm(created_permission)

    await notif_service.send_permission_notification(
        permission=response,
        event_operation=EventOperation.PERMISSION_CREATE
    )

    return response
