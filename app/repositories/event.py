import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.repositories.base import BaseRepository
from app.models.db.event import Event
from app.models.schemas.event import EventInCreate, EventInUpdate
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.utilities.exceptions.database import EntityDoesNotExist


class EventRepository(BaseRepository):
    async def get_events(self) -> typing.Sequence[Event]:
        """Get all events from database"""
        self.logger.debug("Fetching all events from database")

        stmt = sqlalchemy.select(Event)
        query = await self.async_session.execute(statement=stmt)
        events = query.scalars().all()

        self.logger.debug(f"Found {len(events)} events")

        return events

    async def get_events_by_ids(self, event_ids: typing.Sequence[int]) -> typing.Sequence[Event]:
        """Get all events by IDs from database"""
        self.logger.debug(f"Fetching events with IDs {event_ids} from database")

        stmt = sqlalchemy.select(Event).where(Event.id.in_(event_ids))
        query = await self.async_session.execute(statement=stmt)
        events = query.scalars().all()

        self.logger.debug(f"Found {len(events)} events")

        return events

    async def get_events_by_event_type_ids(self, event_type_ids: typing.Sequence[int]) -> typing.Sequence[Event]:
        """Get all events by eventType ID from database"""
        self.logger.debug(f"Fetching events with eventType IDs {event_type_ids} from database")

        stmt = sqlalchemy.select(Event).where(Event.event_type.in_(event_type_ids))
        query = await self.async_session.execute(statement=stmt)
        events = query.scalars().all()

        self.logger.debug(f"Found {len(events)} events")

        return events

    async def get_event_by_id(self, event_id: int) -> Event:
        """Get event by ID from database"""
        self.logger.debug(f"Fetching event with ID {event_id} from database")

        stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=stmt)
        event = query.scalar()

        if not event:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

        self.logger.debug(f"Found event with ID {event_id}")

        return event

    async def get_events_for_user(self, user_id: int) -> typing.Sequence[Event]:
        """Get all events that a user has access to"""
        self.logger.debug(f"Fetching events for user with ID {user_id} from database")

        user_repo = UserRepository(self.async_session)
        user_roles = await user_repo.get_roles_for_user(user_id)

        accessible_event_type_ids = []
        for role in user_roles:
            # Get all eventType IDs where the role has 'can_see' = True
            role_repo = RoleRepository(self.async_session)
            role_event_type_ids = await role_repo.get_event_type_ids_for_role(role.id)
            accessible_event_type_ids.extend(role_event_type_ids)

        accessible_event_type_ids = list(set(accessible_event_type_ids))
        accessible_events = await self.get_events_by_event_type_ids(accessible_event_type_ids)

        self.logger.debug(f"Found {len(accessible_events)} events for user with ID {user_id}")

        return accessible_events

    async def create_event(self, event_create: EventInCreate) -> Event:
        """Create event"""
        self.logger.debug(f"Creating event with data {event_create}")

        new_event = Event(
            created_by=event_create.created_by,
            event_type=event_create.event_type,
            title=event_create.title,
            description=event_create.description,
            start_date=event_create.start_date,
            end_date=event_create.end_date,
        )
        new_event.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_event)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_event)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Created event with ID {new_event.id}")

        return new_event

    async def update_event_by_id(self, event_id: int, event_update: EventInUpdate) -> Event:
        """Update event by ID"""
        self.logger.debug(f"Updating event with ID {event_id} with data {event_update}")

        new_event_data = event_update.dict()

        select_stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_event = query.scalar()

        if not update_event:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

        self.logger.debug(f"Found event with ID {event_id}. Updating...")

        update_stmt = sqlalchemy.update(Event)\
            .where(Event.id == event_id)\
            .values(updated_at=sqlalchemy_functions.now(), **new_event_data)

        await self.async_session.execute(statement=update_stmt)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=update_event)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Updated event with ID {event_id}")

        return update_event

    async def delete_event_by_id(self, event_id: int) -> Event:
        """Delete event by ID"""
        self.logger.debug(f"Deleting event with ID {event_id}")

        stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=stmt)
        event_to_delete = query.scalar()

        if not event_to_delete:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

        self.logger.debug(f"Found event with ID {event_id}. Deleting...")

        delete_stmt = sqlalchemy.delete(Event).where(Event.id == event_id)

        await self.async_session.execute(statement=delete_stmt)
        try:
            await self.async_session.commit()
            self.async_session.expunge(event_to_delete)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Deleted event with ID {event_id}")

        return event_to_delete
