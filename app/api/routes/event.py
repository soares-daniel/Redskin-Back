import fastapi

from app.api.dependencies.repository import get_repository
from app.api.dependencies.service import get_service
from app.models.schemas.event import EventInCreate, EventInResponse, EventInUpdate
from app.models.schemas.event_operation import EventOperation
from app.models.schemas.event_type import EventTypeInResponse
from app.repositories.event import EventRepository
from app.models.db.user import User
from app.api.dependencies.authentication import get_current_user
from app.repositories.event_type import EventTypeRepository
from app.repositories.role_event_type import RoleEventTypeRepository
from app.repositories.user import UserRepository
from app.services.notification import NotificationService
from app.utilities.authorization.permissions import check_event_type_permission
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.http.exc_404 import http_404_exc_event_id_not_found_request

router = fastapi.APIRouter(prefix="/events", tags=["events"])


@router.get(
    path="",
    response_model=list[EventInResponse],
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(get_current_user)]
)
async def get_events(
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> list[EventInResponse]:
    """Get all events"""
    db_events = await event_repo.get_events()

    return [EventInResponse.from_orm(event) for event in db_events]


@router.get(
    path="/event/{event_id}",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(get_current_user)]
)
async def get_event(
        event_id: int,
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> EventInResponse:
    """Get event by id"""
    try:
        db_event = await event_repo.get_event_by_id(event_id)
    except EntityDoesNotExist:
        raise await http_404_exc_event_id_not_found_request(_id=event_id)

    return EventInResponse.from_orm(db_event)


@router.get(
    path="/user",
    response_model=list[EventInResponse],
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(get_current_user)]
)
async def get_events_for_user(
        current_user: User = fastapi.Depends(get_current_user),
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> list[EventInResponse]:
    """Get all events"""
    db_events = await event_repo.get_events_for_user(user_id=current_user.id)
    db_event_list = list()
    for db_event in db_events:
        event = EventInResponse(
            id=db_event.id,
            created_by=db_event.created_by,
            event_type=db_event.event_type,
            title=db_event.title,
            description=db_event.description,
            start_date=db_event.start_date,
            end_date=db_event.end_date,
            created_at=db_event.created_at,
            updated_at=db_event.updated_at,
        )
        db_event_list.append(event)

    return db_event_list


@router.get(
    path="/user/{event_id}",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(get_current_user)]
)
async def get_event_for_user(
        event_id: int,
        current_user: User = fastapi.Depends(get_current_user),
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository)),
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        permission_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository))
) -> EventInResponse:
    """Get event by id"""
    try:
        db_event = await event_repo.get_event_by_id(event_id)
    except EntityDoesNotExist:
        raise await http_404_exc_event_id_not_found_request(_id=event_id)

    await check_event_type_permission(
        user_repo=user_repo, 
        permission_repo=permission_repo, 
        current_user=current_user, 
        event_type=db_event.event_type, 
        action='see'
    )

    return EventInResponse(
        id=db_event.id,
        created_by=db_event.created_by,
        event_type=db_event.event_type,
        title=db_event.title,
        description=db_event.description,
        start_date=db_event.start_date,
        end_date=db_event.end_date,
        created_at=db_event.created_at,
        updated_at=db_event.updated_at,
    )


@router.post(
    path="/create",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
    dependencies=[fastapi.Depends(get_current_user)]
)
async def create_event(
        event_create: EventInCreate,
        current_user: User = fastapi.Depends(get_current_user),
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository)),
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        permission_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> EventInResponse:
    """Create new event"""
    await check_event_type_permission(
        user_repo=user_repo,
        permission_repo=permission_repo,
        current_user=current_user,
        event_type=event_create.event_type,
        action='add'
    )
    db_event = await event_repo.create_event(event_create=event_create)

    response = EventInResponse(
        id=db_event.id,
        created_by=db_event.created_by,
        event_type=db_event.event_type,
        title=db_event.title,
        description=db_event.description,
        start_date=db_event.start_date,
        end_date=db_event.end_date,
        created_at=db_event.created_at,
        updated_at=db_event.updated_at,
    )

    await notif_service.send_event_notification(event=response, event_operation=EventOperation.EVENT_CREATE)

    return response


@router.put(
    path="/update/{event_id}",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(get_current_user)]
)
async def update_event(
        event_id: int,
        event_update: EventInUpdate,
        current_user: User = fastapi.Depends(get_current_user),
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository)),
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        permission_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService))
) -> EventInResponse:
    """Update event"""
    try:
        db_event = await event_repo.get_event_by_id(event_id)

    except EntityDoesNotExist:
        raise await http_404_exc_event_id_not_found_request(_id=event_id)

    await check_event_type_permission(
        user_repo=user_repo,
        permission_repo=permission_repo,
        current_user=current_user,
        event_type=db_event.event_type,
        action='edit'
    )
    updated_event = await event_repo.update_event_by_id(event_id=event_id, event_update=event_update)

    response = EventInResponse(
        id=updated_event.id,
        created_by=updated_event.created_by,
        event_type=updated_event.event_type,
        title=updated_event.title,
        description=updated_event.description,
        start_date=updated_event.start_date,
        end_date=updated_event.end_date,
        created_at=updated_event.created_at,
        updated_at=updated_event.updated_at,
    )

    await notif_service.send_event_notification(event=response, event_operation=EventOperation.EVENT_UPDATE)

    return response


@router.delete(
    path="/delete/{event_id}",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_200_OK,
    dependencies=[fastapi.Depends(get_current_user)]
)
async def delete_event(
        event_id: int,
        current_user: User = fastapi.Depends(get_current_user),
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository)),
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
        permission_repo: RoleEventTypeRepository = fastapi.Depends(get_repository(repo_type=RoleEventTypeRepository)),
        notif_service: NotificationService = fastapi.Depends(get_service(service_type=NotificationService)),
) -> EventInResponse:
    """Delete event"""

    try:
        db_event = await event_repo.get_event_by_id(event_id)

    except EntityDoesNotExist:
        raise await http_404_exc_event_id_not_found_request(_id=event_id)

    await check_event_type_permission(
        user_repo=user_repo,
        permission_repo=permission_repo,
        current_user=current_user,
        event_type=db_event.event_type,
        action='edit'
    )
    deleted_event = await event_repo.delete_event_by_id(event_id)

    response = EventInResponse(
        id=deleted_event.id,
        created_by=deleted_event.created_by,
        event_type=deleted_event.event_type,
        title=deleted_event.title,
        description=deleted_event.description,
        start_date=deleted_event.start_date,
        end_date=deleted_event.end_date,
        created_at=deleted_event.created_at,
        updated_at=deleted_event.updated_at,
    )

    await notif_service.send_event_notification(event=response, event_operation=EventOperation.EVENT_DELETE)

    return response


@router.get(
    path="/event_types",
    response_model=list[EventTypeInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_event_types(
        event_type_repo: EventTypeRepository = fastapi.Depends(get_repository(repo_type=EventTypeRepository)),
) -> list[EventTypeInResponse]:
    """Get event types"""
    event_types = await event_type_repo.get_event_types()
    event_type_list = []
    for event_type in event_types:
        event_type_list.append(EventTypeInResponse(
            id=event_type.id,
            name=event_type.name,
            description=event_type.description,
        ))

    return event_type_list
