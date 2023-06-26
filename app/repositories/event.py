import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.repositories.base import BaseRepository
from app.models.db.event import Event
from app.models.schemas.event import EventInCreate, EventInUpdate
from app.repositories.role import RoleRepository
from app.utilities.exceptions.database import EntityDoesNotExist


class EventRepository(BaseRepository):
    async def get_events(self) -> typing.Sequence[Event]:
        stmt = sqlalchemy.select(Event)
        query = await self.async_session.execute(statement=stmt)
        events = query.scalars().all()

        return events

    async def get_events_by_ids(self, event_ids: typing.Sequence[int]) -> typing.Sequence[Event]:
        stmt = sqlalchemy.select(Event).where(Event.id.in_(event_ids))
        query = await self.async_session.execute(statement=stmt)
        events = query.scalars().all()

        return events

    async def get_events_by_event_type_ids(self, event_type_ids: typing.Sequence[int]) -> typing.Sequence[Event]:
        stmt = sqlalchemy.select(Event).where(Event.event_type.in_(event_type_ids))
        query = await self.async_session.execute(statement=stmt)
        events = query.scalars().all()

        return events

    async def get_event_by_id(self, event_id: int) -> Event:
        stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=stmt)
        event = query.scalar()

        if not event:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

        return event

    async def get_events_for_user(self, user_id: int) -> typing.Sequence[Event]:
        role_repo = RoleRepository(self.async_session)  # Initialize RoleRepository with the same session
        user_roles = await role_repo.get_roles_for_user(user_id)  # Fetch the roles for the user

        accessible_event_type_ids = []
        for role in user_roles:
            # Get all event type ids where the role has 'can_see' = True
            role_event_type_ids = await role_repo.get_event_type_ids_for_role(role.id)
            accessible_event_type_ids.extend(role_event_type_ids)

        accessible_event_type_ids = list(set(accessible_event_type_ids))  # remove duplicates

        # Get all events where the event type id is in `accessible_event_type_ids`
        accessible_events = await self.get_events_by_event_type_ids(accessible_event_type_ids)
        return accessible_events

    async def create_event(self, event_create: EventInCreate) -> Event:
        """Create event"""
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

        return new_event

    async def update_event_by_id(self, event_id: int, event_update: EventInUpdate) -> Event:
        new_event_data = event_update.dict()

        select_stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_event = query.scalar()

        if not update_event:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

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

        return update_event

    async def delete_event_by_id(self, event_id: int) -> Event:
        """Delete event by id"""
        stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=stmt)
        event_to_delete = query.scalar()

        if not event_to_delete:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

        delete_stmt = sqlalchemy.delete(Event).where(Event.id == event_id)

        await self.async_session.execute(statement=delete_stmt)
        try:
            await self.async_session.commit()
            self.async_session.expunge(event_to_delete)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        return event_to_delete
