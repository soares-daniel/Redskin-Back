import fastapi

from app.config.manager import settings
from app.api.dependencies.repository import get_repository
from app.models.schemas.role import RoleInCreate
from app.models.schemas.user import UserInCreate
from app.models.schemas.event_type import EventTypeInCreate
from app.models.schemas.role_event_type import RoleEventTypeInCreate
from app.repositories.user import UserRepository
from app.repositories.role import RoleRepository
from app.repositories.event_type import EventTypeRepository
from app.repositories.role_event_type import RoleEventTypeRepository
from app.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    path="/setup",
    response_model=str,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def setup(
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository)),
        event_type_repo: EventTypeRepository = fastapi.Depends(get_repository(repo_type=EventTypeRepository)),
        role_event_type_repo: RoleEventTypeRepository = fastapi.Depends(
            get_repository(repo_type=RoleEventTypeRepository))
) -> str:
    """Setup endpoint"""

    username = settings.SUPER_USER
    password = settings.SUPER_PASS

    try:
        superuser_obj = await user_repo.get_user_by_username(username)
    except EntityDoesNotExist:
        superuser = UserInCreate(username=username, password=password)
        superuser_obj = await user_repo.create_user(superuser)

    event_type_names = ["scout_event", "comitee_event", "chalet"]
    event_types = []

    for name in event_type_names:
        try:
            event_type_obj = await event_type_repo.get_event_type_by_name(name)
        except EntityDoesNotExist:
            event_type = EventTypeInCreate(name=name)
            event_type_obj = await event_type_repo.create_event_type(event_type)
        event_types.append(event_type_obj)

    role_names = ["admin", "super"]
    roles = []

    for name in role_names:
        try:
            role_obj = await role_repo.get_role_by_name(name)
        except EntityDoesNotExist:
            role = RoleInCreate(name=name)
            role_obj = await role_repo.create_role(role)
        roles.append(role_obj)

    for role in roles:
        if role.name == "super":
            for event_type in event_types:
                role_event_type_data = RoleEventTypeInCreate(
                    role_id=role.id,
                    event_type_id=event_type.id,
                    can_add=True,
                    can_edit=True,
                    can_see=True
                )
                await role_event_type_repo.create_permissions(role_event_type_data)
            await user_repo.assign_role_to_user(user_id=superuser_obj.id, role_id=role.id)

    return "Setup completed successfully"
