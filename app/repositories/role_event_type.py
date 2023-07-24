import typing

import sqlalchemy
from sqlalchemy import func as sqlalchemy_functions

from app.models.db.event_type import EventType
from app.repositories.base import BaseRepository
from app.models.db.role_event_type import RoleEventType
from app.models.schemas.role_event_type import RoleEventTypeInCreate, RoleEventTypeInUpdate
from app.utilities.exceptions.database import EntityDoesNotExist


class RoleEventTypeRepository(BaseRepository):
    async def get_permissions(self) -> typing.Sequence[RoleEventType]:
        """Get all permissions from database"""
        self.logger.debug("Fetching all permissions from database")

        stmt = sqlalchemy.select(RoleEventType)
        query = await self.async_session.execute(statement=stmt)
        permissions = query.scalars().all()

        self.logger.debug(f"Found {len(permissions)} permissions")

        return permissions

    async def get_permissions_by_role_id(self, role_id: int) -> typing.Sequence[RoleEventType]:
        """Get all permissions by role ID from database"""

        self.logger.debug(f"Fetching permissions with role ID {role_id} from database")

        stmt = sqlalchemy.select(RoleEventType).where(RoleEventType.role_id == role_id)
        query = await self.async_session.execute(statement=stmt)
        permissions = query.scalars().all()

        self.logger.debug(f"Found {len(permissions)} permissions")

        return permissions

    async def get_permissions_by_event_type_id(self, event_type_id: int) -> typing.Sequence[RoleEventType]:
        """Get all permissions by event type ID from database"""
        self.logger.debug(f"Fetching permissions with event type ID {event_type_id} from database")

        stmt = sqlalchemy.select(RoleEventType).where(RoleEventType.event_type_id == event_type_id)
        query = await self.async_session.execute(statement=stmt)
        permissions = query.scalars().all()

        self.logger.debug(f"Found {len(permissions)} permissions")

        return permissions

    async def get_permissions_by_role_id_and_event_type_id(self, role_id: int, event_type_id: int) -> RoleEventType:
        """Get permissions by role ID and event type ID from database"""
        self.logger.debug(f"Fetching permissions with role ID {role_id} and event type ID {event_type_id} from database")

        stmt = sqlalchemy.select(RoleEventType)\
            .where(RoleEventType.role_id == role_id)\
            .where(RoleEventType.event_type_id == event_type_id)
        query = await self.async_session.execute(statement=stmt)
        permission = query.scalar()

        self.logger.debug(f"Found permission: {permission}")

        return permission

    async def create_permissions(self, permission_create: RoleEventTypeInCreate) -> RoleEventType:
        """Create new permissions in database"""
        self.logger.debug(f"Creating new permissions: {permission_create}")

        new_permissions = RoleEventType(**permission_create.dict())
        new_permissions.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_permissions)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_permissions)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Created new permissions: {new_permissions}")

        return new_permissions

    async def update_permissions_by_id(
            self,
            role_id: int,
            event_type_id: int,
            permission_update: RoleEventTypeInUpdate
    ) -> RoleEventType:
        """Update permissions by ID in database"""
        self.logger.debug(f"Updating permissions with role ID {role_id} and event type ID {event_type_id} in database")

        update_permissions = await self.get_permissions_by_role_id_and_event_type_id(
            role_id=role_id, event_type_id=event_type_id
        )

        if not update_permissions:
            raise EntityDoesNotExist(f"RoleEventType with role_id {role_id} and event_type_id {event_type_id} does not exist!")

        self.logger.debug(f"Updating permissions: {update_permissions}. Updating...")

        new_permissions_data = permission_update.dict()

        update_stmt = sqlalchemy.update(RoleEventType) \
            .where(RoleEventType.role_id == role_id)\
            .where(RoleEventType.event_type_id == event_type_id)\
            .values(updated_at=sqlalchemy_functions.now(), **new_permissions_data)

        await self.async_session.execute(statement=update_stmt)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=update_permissions)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Updated permissions: {update_permissions}")

        return update_permissions

    async def delete_permissions_by_id(
            self,
            role_id: int,
            event_type_id: int,
    ) -> RoleEventType:
        """Delete permissions by ID in database"""
        self.logger.debug(f"Deleting permissions with role ID {role_id} and event type ID {event_type_id} in database")

        permissions_to_delete = await self.get_permissions_by_role_id_and_event_type_id(
            role_id=role_id, event_type_id=event_type_id
        )

        if not permissions_to_delete:
            raise EntityDoesNotExist(f"RoleEventType with role_id {role_id} and event_type_id {event_type_id} does not exist!")

        self.logger.debug(f"Deleting permissions: {permissions_to_delete}. Deleting...")

        stmt = sqlalchemy.delete(RoleEventType) \
            .where(RoleEventType.role_id == role_id) \
            .where(RoleEventType.event_type_id == event_type_id)

        await self.async_session.execute(statement=stmt)
        try:
            await self.async_session.commit()
            self.async_session.expunge(permissions_to_delete)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Deleted permissions: {permissions_to_delete}")

        return permissions_to_delete

    async def get_event_types_for_role(
            self,
            role_id: int
    ) -> typing.Sequence[EventType]:
        """Get all event types by role from database"""
        self.logger.debug("Fetching all event types by role from database")

        stmt = sqlalchemy.select(EventType).join(RoleEventType).where(RoleEventType.role_id == role_id)
        query = await self.async_session.execute(statement=stmt)
        event_types = query.scalars().all()

        self.logger.debug(f"Found {len(event_types)} event types")

        return event_types
