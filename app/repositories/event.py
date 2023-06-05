from typing import Sequence

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.repositories.base import BaseRepository
from app.models.db.event import Event
from app.models.schemas.event import EventInCreate, EventInUpdate
from app.utilities.exceptions.database import EntityDoesNotExist


class EventRepository(BaseRepository):
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
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_event)

        return new_event

    async def get_events(self) -> Sequence[Event]:
        stmt = sqlalchemy.select(Event)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def get_event_by_id(self, event_id: int) -> Event:
        stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

        return query.scalar()

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
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_event)

        return update_event

    async def delete_event_by_id(self, event_id: int) -> bool:
        select_stmt = sqlalchemy.select(Event).where(Event.id == event_id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_event = query.scalar()

        if not delete_event:
            raise EntityDoesNotExist(f"Event with id {event_id} does not exist!")

        delete_stmt = sqlalchemy.delete(Event).where(Event.id == event_id)
        await self.async_session.execute(statement=delete_stmt)
        await self.async_session.commit()

        return True
