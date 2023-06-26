import typing

import sqlalchemy
from sqlalchemy import func as sqlalchemy_functions

from app.models.db.event_type import EventType
from app.models.schemas.event_type import EventTypeInCreate, EventTypeInUpdate
from app.repositories.base import BaseRepository
from app.utilities.exceptions.database import EntityDoesNotExist


class EventTypeRepository(BaseRepository):
    async def get_event_types(self) -> typing.Sequence[EventType]:
        stmt = sqlalchemy.select(EventType)
        query = await self.async_session.execute(statement=stmt)
        event_types = query.scalars().all()

        return event_types

    async def get_event_type_by_id(self, event_type_id: int) -> EventType:
        stmt = sqlalchemy.select(EventType).where(EventType.id == event_type_id)
        query = await self.async_session.execute(statement=stmt)
        event_type = query.scalar()

        if not event_type:
            raise EntityDoesNotExist(f"Event type with id {event_type_id} does not exist!")

        return event_type

    async def get_event_type_by_name(self, event_type_name: str) -> EventType:
        stmt = sqlalchemy.select(EventType).where(EventType.name == event_type_name)
        query = await self.async_session.execute(statement=stmt)
        event_type = query.scalar()

        if not event_type:
            raise EntityDoesNotExist(f"Event type with name {event_type_name} does not exist!")

        return event_type

    async def create_event_type(self, event_type_create: EventTypeInCreate) -> EventType:
        new_event_type = EventType(**event_type_create.dict())
        new_event_type.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_event_type)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_event_type)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        return new_event_type

    async def update_event_type_by_id(self, event_type_id: int, event_type_update: EventTypeInUpdate) -> EventType:
        select_stmt = sqlalchemy.select(EventType).where(EventType.id == event_type_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_event_type = query.scalar()

        if not update_event_type:
            raise EntityDoesNotExist(f"EventType with id {event_type_id} does not exist!")

        new_event_type_data = event_type_update.dict()

        update_stmt = sqlalchemy.update(EventType) \
            .where(EventType.id == event_type_id) \
            .values(updated_at=sqlalchemy_functions.now(), **new_event_type_data)

        await self.async_session.execute(statement=update_stmt)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=update_event_type)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        return update_event_type

    async def delete_event_type_by_id(self, event_type_id: int) -> EventType:
        select_stmt = sqlalchemy.select(EventType).where(EventType.id == event_type_id)
        query = await self.async_session.execute(statement=select_stmt)
        event_type_to_delete = query.scalar()

        if not event_type_to_delete:
            raise EntityDoesNotExist(f"EventType with id {event_type_id} does not exist!")

        stmt = sqlalchemy.delete(EventType).where(EventType.id == event_type_id)

        await self.async_session.execute(statement=stmt)
        try:
            await self.async_session.commit()
            self.async_session.expunge(event_type_to_delete)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        return event_type_to_delete
