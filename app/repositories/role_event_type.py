import typing

import sqlalchemy
from sqlalchemy import func as sqlalchemy_functions

from app.repositories.base import BaseRepository
from app.models.db.role_event_type import RoleEventType
from app.models.schemas.role_event_type import RoleEventTypeInCreate, RoleEventTypeInUpdate
from app.utilities.exceptions.database import EntityDoesNotExist


class RoleEventTypeRepository(BaseRepository):
    async def get_permissions_by_role_id(self, role_id: int) -> typing.Sequence[RoleEventType]:
        stmt = sqlalchemy.select(RoleEventType).where(RoleEventType.role_id == role_id)
        query = await self.async_session.execute(statement=stmt)
        permissions = query.scalars().all()

        return permissions

    async def get_permissions_by_event_type_id(self, event_type_id: int) -> typing.Sequence[RoleEventType]:
        stmt = sqlalchemy.select(RoleEventType).where(RoleEventType.event_type_id == event_type_id)
        query = await self.async_session.execute(statement=stmt)
        permissions = query.scalars().all()

        return permissions

    async def get_permissions_by_role_id_and_event_type_id(self, role_id: int, event_type_id: int) -> RoleEventType:
        stmt = sqlalchemy.select(RoleEventType)\
            .where(RoleEventType.role_id == role_id)\
            .where(RoleEventType.event_type_id == event_type_id)
        query = await self.async_session.execute(statement=stmt)
        permission = query.scalar()

        return permission

    async def create_permissions(self, permission_create: RoleEventTypeInCreate) -> RoleEventType:
        new_permissions = RoleEventType(**permission_create.dict())
        new_permissions.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_permissions)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_permissions)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        return new_permissions

    async def update_permissions_by_id(
            self,
            role_id: int,
            event_type_id: int,
            permission_update: RoleEventTypeInUpdate
    ) -> RoleEventType:
        select_stmt = sqlalchemy.select(RoleEventType)\
            .where(RoleEventType.role_id == role_id)\
            .where(RoleEventType.event_type_id == event_type_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_permissions = query.scalar()

        if not update_permissions:
            raise EntityDoesNotExist(f"RoleEventType with role_id {role_id} and event_type_id {event_type_id} does not exist!")

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

        return update_permissions

    async def delete_permissions_by_id(
            self,
            role_id: int,
            event_type_id: int,
    ) -> RoleEventType:
        select_stmt = sqlalchemy.select(RoleEventType)\
            .where(RoleEventType.role_id == role_id)\
            .where(RoleEventType.event_type_id == event_type_id)
        query = await self.async_session.execute(statement=select_stmt)
        permissions_to_delete = query.scalar()

        if not permissions_to_delete:
            raise EntityDoesNotExist(f"RoleEventType with role_id {role_id} and event_type_id {event_type_id} does not exist!")

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

        return permissions_to_delete
