from app.models.db.user import User
from app.repositories.role_event_type import RoleEventTypeRepository
from app.repositories.user import UserRepository
from app.utilities.exceptions.http.exc_403 import http_403_exc_permission_denied


# TODO: Optimize this function
async def check_event_type_permission(
        user_repo: UserRepository,
        permission_repo: RoleEventTypeRepository,
        current_user: User,
        event_type: int,
        action: str
) -> None:
    """Check if a user has permission to perform an action on an event type."""
    # Get roles for user
    roles = await user_repo.get_roles_for_user(user_id=current_user.id)

    # Check if user has permission to perform action on event type
    for role in roles:
        permissions = await permission_repo.get_permissions_by_role_id(role_id=role.id)
        for permission in permissions:
            if permission.event_type_id == event_type:
                if action == "add":
                    if permission.can_add:
                        return
                elif action == "see":
                    if permission.can_see:
                        return
                elif action == "edit":
                    if permission.can_see:
                        return
    raise http_403_exc_permission_denied()
