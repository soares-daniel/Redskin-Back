import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.models.db.user import User
from app.repositories.base import BaseRepository
from app.models.db.role import Role
from app.models.schemas.role import RoleInCreate, RoleInUpdate
from app.utilities.exceptions.database import EntityDoesNotExist


class RoleRepository(BaseRepository):
    async def get_roles(self) -> typing.Sequence[Role]:
        stmt = sqlalchemy.select(Role)
        query = await self.async_session.execute(statement=stmt)
        roles = query.scalars().all()

        return roles

    async def get_role_by_id(self, role_id: int) -> Role:
        stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        query = await self.async_session.execute(statement=stmt)
        role = query.scalar()

        if not role:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

        return role

    async def get_role_by_name(self, role_name: str) -> Role:
        stmt = sqlalchemy.select(Role).where(Role.name == role_name)
        query = await self.async_session.execute(statement=stmt)
        role = query.scalar()

        if not role:
            raise EntityDoesNotExist(f"Role with name {role_name} does not exist!")

        return role

    async def create_role(self, role_create: RoleInCreate) -> Role:
        new_role = Role(**role_create.dict())
        new_role.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_role)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_role)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        return new_role

    async def update_role_by_id(self, role_id: int, role_update: RoleInUpdate) -> Role:
        select_stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_role = query.scalar()

        if not update_role:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

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

        return update_role

    async def delete_role_by_id(self, role_id: int) -> Role:
        select_stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        query = await self.async_session.execute(statement=select_stmt)
        role_to_delete = query.scalar()

        if not role_to_delete:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

        stmt = sqlalchemy.delete(Role).where(Role.id == role_id)

        await self.async_session.execute(statement=stmt)
        try:
            await self.async_session.commit()
            self.async_session.expunge(role_to_delete)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        return role_to_delete

    async def get_event_type_ids_for_role(self, role_id: int) -> typing.Sequence[int]:
        role_stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        role_query = await self.async_session.execute(role_stmt)
        role = role_query.scalar()

        if not role:
            raise EntityDoesNotExist(f"Role with id {role_id} does not exist!")

        return [event_type.id for event_type in role.event_types]
