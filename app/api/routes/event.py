import fastapi

from app.api.dependencies.repository import get_repository
from app.models.schemas.event import EventInCreate, EventInResponse, EventInUpdate
from app.repositories.event import EventRepository
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request
from app.utilities.exceptions.http.exc_500 import http_500_exc_internal_server_error
router = fastapi.APIRouter(prefix="/events", tags=["events"])


@router.get(
    path="",
    response_model=list[EventInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_events(
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> list[EventInResponse]:
    """Get all events"""
    db_events = await event_repo.get_events()
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
    path="/{event_id}",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_event(
        event_id: int,
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> EventInResponse:
    """Get event by id"""
    try:
        db_event = await event_repo.get_event_by_id(event_id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(_id=event_id)

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
    path="",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_event(
        event_create: EventInCreate,
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> EventInResponse:
    """Create new event"""
    db_event = await event_repo.create_event(event_create=event_create)

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


@router.put(
    path="/{event_id}",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_event(
        event_id: int,
        event_update: EventInUpdate,
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> EventInResponse:
    """Update event"""
    try:
        db_event = await event_repo.get_event_by_id(event_id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(_id=event_id)

    updated_event = await event_repo.update_event_by_id(event_id=event_id, event_update=event_update)

    if updated_event is None:
        raise await http_500_exc_internal_server_error()

    return EventInResponse(
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


@router.delete(
    path="/{event_id}",
    response_model=EventInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_event(
        event_id: int,
        event_repo: EventRepository = fastapi.Depends(get_repository(repo_type=EventRepository))
) -> EventInResponse:
    """Delete event"""
    raise NotImplementedError
