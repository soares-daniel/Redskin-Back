import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.models.schemas.user_role import UserRoleInAssign, UserRoleInRemove
from app.repositories.base import BaseRepository
from app.models.db.role import Role
from app.models.db.user import User
from app.models.db.user_role import user_roles
from app.models.schemas.user import UserInCreate, UserInLogin, UserInUpdate
from app.security.hashing.password import pass_generator
from app.security.verifications.credentials import credential_verifier
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.security import PasswordDoesNotMatch


class UserRepository(BaseRepository):
    async def get_users(self) -> typing.Sequence[User]:
        """Get all users from database"""
        self.logger.debug("Fetching all users from database")

        stmt = (sqlalchemy.select(User)
                .where(~User.first_name.is_(None), ~User.last_name.is_(None))  # type: ignore
                .order_by(User.id))
        query = await self.async_session.execute(statement=stmt)
        users = query.scalars().all()

        self.logger.debug(f"Found {len(users)} users")

        return users

    async def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID from database"""
        self.logger.debug(f"Fetching user with ID {user_id} from database")

        stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.async_session.execute(statement=stmt)
        user = query.scalar()

        if not user:
            raise EntityDoesNotExist(f"User with id {user_id} does not exist!")

        self.logger.debug(f"Found user with ID {user_id}")

        return user

    async def get_user_by_username(self, username: str) -> User:
        """Get user by username from database"""
        self.logger.debug(f"Fetching user with username {username} from database")

        stmt = (sqlalchemy.select(User).where(User.username == username))
        query = await self.async_session.execute(statement=stmt)
        user = query.scalar()

        if not user:
            raise EntityDoesNotExist(f"User with username {username} does not exist!")

        self.logger.debug(f"Found user with username {username}")

        return user

    async def read_user_by_password_authentication(self, user_login: UserInLogin) -> User:
        """Get user by username and password from database"""
        self.logger.debug(f"Fetching user with username {user_login.username} from database")

        stmt = sqlalchemy.select(User).where(User.username == user_login.username)
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist(f"Wrong username")

        self.logger.debug(f"Found user with username {user_login.username}. Verifying password...")

        if not pass_generator.is_password_authenticated(
                salt=db_user.hash_salt,
                password=user_login.password,
                hashed_password=db_user.hashed_password,
        ):
            raise PasswordDoesNotMatch("Password does not match!")

        self.logger.debug(f"User with username {user_login.username} authenticated")

        return db_user

    async def create_user(self, user_create: UserInCreate) -> User:
        """Create user"""
        self.logger.debug(f"Creating user with username {user_create.username}")

        # If user has firstname, user has to have lastname and visa versa, else raise exception
        if (user_create.first_name is None and user_create.last_name is not None) or \
                (user_create.first_name is not None and user_create.last_name is None):
            raise ValueError("User has to have both first and last name or neither")

        new_user = User(
            username=user_create.username,
            first_name=user_create.first_name,
            last_name=user_create.last_name
        )
        new_user.set_hash_salt(hash_salt=pass_generator.generate_salt)
        new_user.set_hashed_password(
            hashed_password=pass_generator.generate_hashed_password(
                salt=new_user.hash_salt, password=user_create.password
            )
        )
        new_user.created_at = sqlalchemy_functions.now()

        self.async_session.add(instance=new_user)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_user)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Created user with username {user_create.username}")

        return new_user

    async def update_user_by_id(self, user_id: int, user_update: UserInUpdate) -> User:
        """Update user by ID"""
        self.logger.debug(f"Updating user with ID {user_id}")

        new_user_data = user_update.dict()

        select_stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_user = query.scalar()

        if not update_user:
            raise EntityDoesNotExist(f"User with id {user_id} does not exist!")

        self.logger.debug(f"Found user with ID {user_id}")

        update_stmt = sqlalchemy.update(User) \
            .where(User.id == update_user.id) \
            .values(updated_at=sqlalchemy_functions.now())

        if new_user_data.get("username"):
            self.logger.debug(f"Updating username to {new_user_data['username']}")
            update_stmt = update_stmt.values(username=new_user_data["username"])

        if new_user_data.get("first_name"):
            self.logger.debug(f"Updating first_name to {new_user_data['first_name']}")
            update_stmt = update_stmt.values(first_name=new_user_data["first_name"])

        if new_user_data.get("last_name"):
            self.logger.debug(f"Updating last_name to {new_user_data['last_name']}")
            update_stmt = update_stmt.values(last_name=new_user_data["last_name"])

        if new_user_data.get("password"):
            self.logger.debug(f"Updating password to '********' ;)")
            update_stmt = update_stmt.values(
                hash_salt=pass_generator.generate_salt,
                hashed_password=pass_generator.generate_hashed_password(
                    salt=update_user.hash_salt, password=new_user_data["password"]
                ),
            )

        await self.async_session.execute(statement=update_stmt)
        try:
            await self.async_session.commit()
            await self.async_session.refresh(instance=update_user)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Updated user with ID {user_id}")

        return update_user

    async def delete_user_by_id(self, user_id: int) -> User:
        """Delete user by ID"""
        self.logger.debug(f"Deleting user with ID {user_id}")

        select_stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_user = query.scalar()

        if not delete_user:
            raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

        self.logger.debug(f"Found user with ID {user_id}")

        stmt = sqlalchemy.delete(table=User).where(User.id == delete_user.id)
        await self.async_session.execute(statement=stmt)
        try:
            await self.async_session.commit()
            self.async_session.expunge(delete_user)
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Deleted user with ID {user_id}")

        return delete_user

    async def is_username_taken(self, username: str) -> bool:
        """Check if username is taken"""
        self.logger.debug(f"Checking if username {username} is taken")

        username_stmt = sqlalchemy.select(User.username).select_from(User).where(User.username == username)
        username_query = await self.async_session.execute(username_stmt)
        db_username = username_query.scalar()

        if not credential_verifier.is_username_available(username=db_username):
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")

        self.logger.debug(f"Username {username} is available")

        return True

    async def assign_role_to_user(self, user_id: int, role_id: int) -> UserRoleInAssign:
        """Assign role to user"""
        self.logger.debug(f"Assigning role with ID {role_id} to user with ID {user_id}")

        self.logger.debug(f"Checking if user with ID {user_id} exists")
        user_stmt = sqlalchemy.select(User).where(User.id == user_id)
        user_query = await self.async_session.execute(user_stmt)
        user = user_query.scalar_one_or_none()

        self.logger.debug(f"Checking if role with ID {role_id} exists")
        role_stmt = sqlalchemy.select(Role).where(Role.id == role_id)
        role_query = await self.async_session.execute(role_stmt)
        role = role_query.scalar_one_or_none()

        if user is None or role is None:
            raise EntityDoesNotExist(f"User with id {user_id} or Role with id {role_id} does not exist!")

        self.logger.debug(f"Found user with ID {user_id} and role with ID {role_id}")

        # Assign the role to the user by inserting a new row into user_roles
        stmt = user_roles.insert().values(USER_ID=user_id, ROLE_ID=role_id)
        try:
            await self.async_session.execute(stmt)
            await self.async_session.commit()
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Assigned role with ID {role_id} to user with ID {user_id}")

        return UserRoleInAssign(username=user.username, role_name=role.name)

    async def remove_role_from_user(self, user_id: int, role_id: int) -> UserRoleInRemove:
        """Remove role from user"""
        self.logger.debug(f"Removing role with ID {role_id} from user with ID {user_id}")

        self.logger.debug(f"Checking if user with ID {user_id} exists")
        stmt = sqlalchemy.select(user_roles).where(user_roles.c.USER_ID == user_id, user_roles.c.ROLE_ID == role_id)
        query = await self.async_session.execute(stmt)
        user_role = query.scalar_one_or_none()

        if user_role is None:
            raise EntityDoesNotExist(f"User with id {user_id} and Role with id {role_id} are not related!")

        self.logger.debug(f"Found user with ID {user_id} and role with ID {role_id}")

        # Remove the role from the user by deleting the row from user_roles
        stmt = user_roles.delete().where(user_roles.c.USER_ID == user_id, user_roles.c.ROLE_ID == role_id)
        try:
            await self.async_session.execute(stmt)
            await self.async_session.commit()
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Removed role with ID {role_id} from user with ID {user_id}")

        return UserRoleInRemove(username=user_role.username, role_name=user_role.role_name)

    async def get_roles_for_user(self, user_id: int) -> typing.Sequence[Role]:
        """Get roles for user"""
        self.logger.debug(f"Getting roles for user with ID {user_id}")

        stmt = sqlalchemy.select(user_roles.c.ROLE_ID).where(user_roles.c.USER_ID == user_id)
        result = await self.async_session.execute(stmt)
        role_ids = [row[0] for row in result]

        if not role_ids:
            raise EntityDoesNotExist(f"User has no roles!")

        self.logger.debug(f"Found role IDs for user with ID {user_id}")

        # Fetch the actual Role objects using the role_ids
        roles_stmt = sqlalchemy.select(Role).where(Role.id.in_(role_ids))  # type: ignore
        roles_result = await self.async_session.execute(roles_stmt)
        roles = roles_result.scalars().all()

        self.logger.debug(f"Found roles for user with ID {user_id}")

        return roles
