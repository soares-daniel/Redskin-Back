from typing import Sequence

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.repositories.base import BaseRepository
from app.models.db.user import User
from app.models.schemas.user import UserInCreate, UserInLogin, UserInUpdate
from app.security.hashing.password import pass_generator
from app.security.verifications.credentials import credential_verifier
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.security import PasswordDoesNotMatch


class UserRepository(BaseRepository):
    async def create_user(self, user_create: UserInCreate) -> User:
        """Create user"""
        new_user = User(username=user_create.username)
        new_user.set_hash_salt(hash_salt=pass_generator.generate_salt)
        new_user.set_hashed_password(
            hashed_password=pass_generator.generate_hashed_password(
                salt=new_user.hash_salt, password=user_create.password
            )
        )
        new_user.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_user)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_user)

        return new_user

    async def get_users(self) -> Sequence[User]:
        stmt = sqlalchemy.select(User)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"User with id {user_id} does not exist!")

        return query.scalar()  # type: ignore

    async def get_user_by_username(self, username: str) -> User:
        stmt = sqlalchemy.select(User).where(User.username == username)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"User with username {username} does not exist!")

        return query.scalar()  # type: ignore

    async def get_user_by_password_authentication(self, user_login: UserInLogin) -> User:
        stmt = sqlalchemy.select(User).where(User.username == user_login.username)
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist(f"Wrong username")

        if not pass_generator.is_password_authenticated(
            salt=db_user.hash_salt,
            password=user_login.password,
            hashed_password=db_user.hashed_password,
        ):
            raise PasswordDoesNotMatch("Password does not match!")

        return db_user

    async def update_user_by_id(self, user_id: int, user_update: UserInUpdate) -> User:
        new_user_data = user_update.dict()

        select_stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_user = query.scalar()

        if not update_user:
            raise EntityDoesNotExist(f"User with id {user_id} does not exist!")

        update_stmt = sqlalchemy.update(User)\
            .where(User.id == update_user.id)\
            .values(updated_at=sqlalchemy_functions.now())

        if new_user_data.get("username"):
            update_stmt = update_stmt.values(username=new_user_data["username"])

        if new_user_data.get("password"):
            update_stmt = update_stmt.values(
                hash_salt=pass_generator.generate_salt,
                hashed_password=pass_generator.generate_hashed_password(
                    salt=update_user.hash_salt, password=new_user_data["password"]
                ),
            )

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_user)

        return update_user

    async def delete_user_by_id(self, user_id: int) -> bool:
        select_stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_user = query.scalar()

        if not delete_user:
            raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

        stmt = sqlalchemy.delete(table=User).where(User.id == delete_user.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return True

    async def is_username_taken(self, username: str) -> bool:
        username_stmt = sqlalchemy.select(User.username).select_from(User).where(User.username == username)
        username_query = await self.async_session.execute(username_stmt)
        db_username = username_query.scalar()

        if not credential_verifier.is_username_available(username=db_username):
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")

        return True
