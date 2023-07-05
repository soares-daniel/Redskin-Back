from enum import Enum


class EventOperation(Enum):
    EVENT_CREATE = "event_create"
    EVENT_UPDATE = "event_update"
    EVENT_DELETE = "event_delete"
    EVENT_TYPE_CREATE = "event_type_create"
    EVENT_TYPE_UPDATE = "event_type_update"
    EVENT_TYPE_DELETE = "event_type_delete"
    ROLE_CREATE = "role_create"
    ROLE_UPDATE = "role_update"
    ROLE_DELETE = "role_delete"
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    USER_ROLE_ASSIGN = "user_role_assign"
    USER_ROLE_REMOVE = "user_role_remove"
    PERMISSION_CREATE = "permission_create"
    PERMISSION_UPDATE = "permission_update"
    PERMISSION_DELETE = "permission_delete"
