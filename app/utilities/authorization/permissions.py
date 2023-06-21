from app.models.db.event import Event
from app.models.db.user import User
from app.utilities.exceptions.http.exc_403 import http_403_exc_permission_denied


async def check_event_type_permission(current_user: User, event_type: int, action: str) -> None:
    """Check if a user has permission to perform an action on an event type."""
    for role in current_user.roles:
        for role_event_type in role.event_types:
            if role_event_type.event_type_id == event_type:
                if ((action == 'see' and role_event_type.can_see) or
                        (action == 'edit' and role_event_type.can_edit) or
                        (action == 'add' and role_event_type.can_add)):
                    return
    raise http_403_exc_permission_denied()