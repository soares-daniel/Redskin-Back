import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.models.db.role_event_type import RoleEventType
from app.repositories.base import BaseRepository
from app.models.db.role import Role
from app.models.schemas.role import RoleInCreate, RoleInUpdate
from app.utilities.exceptions.database import EntityDoesNotExist


class RoleRepository(BaseRepository):
    async def get_roles(self) -> typing.Sequence[Role]:
        """Get all roles from database"""
        self.logger.debug("Fetching all roles from database")

        stmt = sqlalchemy.select(Role)
        query = await self.async_session.execute(statement=stmt)
        roles = query.scalars().all()

        self.logger.debug(f"Found {len(roles)} roles")

        return roles

    async def get_role_by_id(self, role_id: int) -> Role:
        """Get role by ID from database"""
        self.logger.debug(f"Fetching role with ID {role_id} from database")

        stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        query = await self.async_session.execute(statement=stmt)
        role = query.scalar()

        if not role:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

        self.logger.debug(f"Found role with ID {role_id}")

        return role

    async def get_role_by_name(self, role_name: str) -> Role:
        """Get role by name from database"""
        self.logger.debug(f"Fetching role with name {role_name} from database")

        stmt = sqlalchemy.select(Role).where(Role.name == role_name)
        query = await self.async_session.execute(statement=stmt)
        role = query.scalar()

        if not role:
            raise EntityDoesNotExist(f"Role with name {role_name} does not exist!")

        self.logger.debug(f"Found role with name {role_name}")

        return role

    async def create_role(self, role_create: RoleInCreate) -> Role:
        """Create role in database"""
        self.logger.debug(f"Creating role with name {role_create.name} in database")

        new_role = Role(**role_create.dict())
        new_role.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_role)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_role)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Created role with name {role_create.name} in database")

        return new_role

    async def update_role_by_id(self, role_id: int, role_update: RoleInUpdate) -> Role:
        """Update role by ID in database"""
        self.logger.debug(f"Updating role with ID {role_id} in database")

        select_stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_role = query.scalar()

        if not update_role:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

        self.logger.debug(f"Found role with ID {role_id}. Updating...")

        new_role_data = role_update.dict()

        update_stmt = sqlalchemy.update(Role) \
            .where(Role.id == role_id) \
            .values(updated_at=sqlalchemy_functions.now(), **new_role_data)

        await self.async_session.execute(statement=update_stmt)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=update_role)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Updated role with ID {role_id} in database")

        return update_role

    async def delete_role_by_id(self, role_id: int) -> Role:
        """Delete role by ID from database"""
        self.logger.debug(f"Deleting role with ID {role_id} from database")

        select_stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        query = await self.async_session.execute(statement=select_stmt)
        role_to_delete = query.scalar()

        if not role_to_delete:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

        self.logger.debug(f"Found role with ID {role_id}. Deleting...")

        stmt = sqlalchemy.delete(Role).where(Role.id == role_id)

        await self.async_session.execute(statement=stmt)
        try:
            await self.async_session.commit()
            self.async_session.expunge(role_to_delete)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Deleted role with ID {role_id} from database")

        return role_to_delete

    async def get_event_type_ids_for_role(self, role_id: int) -> typing.Sequence[int]:
        """Get event type IDs for role from database"""
        self.logger.debug(f"Fetching event type IDs for role with ID {role_id} from database")

        role_stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        role_query = await self.async_session.execute(role_stmt)
        role = role_query.scalar()

        if not role:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

        self.logger.debug(f"Found role with ID {role_id}. Fetching event type IDs...")

        event_type_stmt = sqlalchemy.select(RoleEventType).where(RoleEventType.role_id == role_id)
        event_type_query = await self.async_session.execute(event_type_stmt)
        event_type_ids = [role_event_type.event_type_id for role_event_type in event_type_query.scalars().all()]

        self.logger.debug(f"Found {len(event_type_ids)} event type IDs for role with ID {role_id}")

        return event_type_ids
