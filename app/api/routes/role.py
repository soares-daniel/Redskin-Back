import fastapi

from app.api.dependencies.repository import get_repository
from app.api.dependencies.role import is_user_in_role
from app.api.dependencies.service import get_service
from app.models.schemas.event_operation import EventOperation
from app.models.schemas.role import RoleInCreate, RoleInResponse, RoleInUpdate
from app.models.schemas.role_event_type import RoleEventTypeInResponse, RoleEventTypeInCreate
from app.repositories.role import RoleRepository
from app.models.db.user import User
from app.api.dependencies.authentication import get_current_user
from app.repositories.role_event_type import RoleEventTypeRepository
from app.services.notification import NotificationService
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.http.exc_404 import http_404_exc_user_id_not_found_request
from app.utilities.exceptions.http.exc_500 import http_500_exc_internal_server_error

router = fastapi.APIRouter(prefix="/roles", tags=["roles"])


@router.get(
    path="",
    response_model=list[RoleInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_roles(
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository))
) -> list[RoleInResponse]:
    """Get all roles"""
    db_roles = await role_repo.get_roles()

    return [RoleInResponse.from_orm(role) for role in db_roles]


@router.get(
    path="/role/{role_id}",
    response_model=RoleInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_role(
        role_id: int,
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository))
) -> RoleInResponse:
    """Get role by id"""
    try:
        db_role = await role_repo.get_role_by_id(role_id)
    except EntityDoesNotExist:
        raise await http_404_exc_user_id_not_found_request(_id=role_id)

    return RoleInResponse.from_orm(db_role)


@router.get(
    path="/permissions",
    response_model=list[RoleEventTypeInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_permissions(
        role_event_type_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository))
) -> list[RoleEventTypeInResponse]:
    """Get all event types"""
    db_event_types = await role_event_type_repo.get_permissions()

    return [RoleEventTypeInResponse.from_orm(role_event_type) for role_event_type in db_event_types]


@router.get(
    path="/role/{role_id}/permissions",
    response_model=list[RoleEventTypeInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_permissions_by_role_id(
        role_id: int,
        role_event_type_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository))
) -> list[RoleEventTypeInResponse]:
    """Get all event types by role id"""
    db_event_types = await role_event_type_repo.get_permissions_by_role_id(role_id)

    return [RoleEventTypeInResponse.from_orm(role_event_type) for role_event_type in db_event_types]
