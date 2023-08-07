import fastapi

from app.api.dependencies.role import is_user_in_role
from app.config.manager import settings
from app.api.dependencies.repository import get_repository
from app.models.db.user import User
from app.models.schemas.role import RoleInCreate
from app.models.schemas.user import UserInCreate
from app.models.schemas.event_type import EventTypeInCreate
from app.models.schemas.role_event_type import RoleEventTypeInCreate
from app.repositories.user import UserRepository
from app.repositories.role import RoleRepository
from app.repositories.event_type import EventTypeRepository
from app.repositories.role_event_type import RoleEventTypeRepository
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists

router = fastapi.APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    path="/setup",
    response_model=str,
    status_code=fastapi.status.HTTP_201_CREATED,
    dependencies=[fastapi.Depends(is_user_in_role(role="NEVERRR"))],
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

    event_type_names = {"scout_event": "Pfadfindertermine", "committee_event": "Vorstandtermine", "chalet": "Chaletvermietung"}
    event_types = []
    role_names = ["super"]
    roles = []

    try:
        user = await user_repo.get_user_by_username(username=username)
    except EntityDoesNotExist:
        user: User = await user_repo.create_user(user_create=UserInCreate(username=username, password=password))

    for role_name in role_names:
        try:
            role = await role_repo.get_role_by_name(role_name=role_name)
        except EntityDoesNotExist:
            role = await role_repo.create_role(role_create=RoleInCreate(name=role_name))
        roles.append(role)

    for event_type in event_type_names:
        for event_type_name, description in event_type_names.items():
            try:
                event_type = await event_type_repo.get_event_type_by_name(event_type_name=event_type_name)
            except EntityDoesNotExist:
                event_type = await event_type_repo.create_event_type(
                    event_type_create=EventTypeInCreate(name=event_type_name, description=description)
                )
            event_types.append(event_type)

    for role in roles:
        try:
            await user_repo.assign_role_to_user(user_id=user.id, role_id=role.id)
        except EntityAlreadyExists:
            pass
        for event_type in event_types:
            await role_event_type_repo.create_permissions(
                permission_create=RoleEventTypeInCreate(
                    role_id=role.id,
                    event_type_id=event_type.id,
                    can_edit=True,
                    can_see=True,
                    can_add=True
                ))

    return "Setup complete!"


@router.post(
    path="/roles",
    response_model=str,
    status_code=fastapi.status.HTTP_201_CREATED,
    dependencies=[fastapi.Depends(is_user_in_role(role="NEVERRR"))],
)
async def roles(
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository)),
        event_type_repo: EventTypeRepository = fastapi.Depends(get_repository(repo_type=EventTypeRepository)),
        role_event_type_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository))
) -> str:
    """Create a new role"""

    role_names = ["chefleitung", "chef", "chefassistent", "committee", "chalet"]

    roles = []
    for role_name in role_names:
        try:
            role = await role_repo.get_role_by_name(role_name=role_name)
        except EntityDoesNotExist:
            role = await role_repo.create_role(role_create=RoleInCreate(name=role_name))
        roles.append(role)

    event_types = await event_type_repo.get_event_types()

    for event_type in event_types:
        if event_type.name == "scout_event":
            for role in roles:
                if role.name == "chefleitung":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=True,
                            can_see=True,
                            can_add=True
                        ))
                elif role.name == "chef":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=True,
                            can_see=True,
                            can_add=True
                        ))
                elif role.name == "chefassistent":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=False,
                            can_see=True,
                            can_add=False
                        ))
                elif role.name == "committee":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=False,
                            can_see=True,
                            can_add=False
                        ))
        elif event_type.name == "comitee_event":
            for role in roles:
                if role.name == "chefleitung":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=False,
                            can_see=True,
                            can_add=False
                        ))
                elif role.name == "committee":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=True,
                            can_see=True,
                            can_add=True
                        ))
        elif event_type.name == "chalet":
            for role in roles:
                if role.name == "chefleitung":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=False,
                            can_see=True,
                            can_add=False
                        ))
                elif role.name == "chalet":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=False,
                            can_see=True,
                            can_add=False
                        ))
                elif role.name == "chefassistent":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=False,
                            can_see=True,
                            can_add=False
                        ))
                elif role.name == "committee":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=False,
                            can_see=True,
                            can_add=False
                        ))
                elif role.name == "chalet":
                    await role_event_type_repo.create_permissions(
                        permission_create=RoleEventTypeInCreate(
                            role_id=role.id,
                            event_type_id=event_type.id,
                            can_edit=True,
                            can_see=True,
                            can_add=True
                        ))

    return "Roles created!"