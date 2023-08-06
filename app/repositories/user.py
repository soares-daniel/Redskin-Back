import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy import and_, select
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

        # If user has firstname, user has to have lastname and visa-versa, else raise exception
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

        values_to_update = {}
        for field, value in new_user_data.items():
            if value is not None:
                self.logger.debug(f"Updating {field} to {value}")
                values_to_update[field] = value

        values_to_update['updated_at'] = sqlalchemy_functions.now()

        update_stmt = (
            sqlalchemy.update(User)
            .where(User.id == user_id)
            .values(**values_to_update)
        )

        try:
            await self.async_session.execute(update_stmt)
            await self.async_session.commit()
        except Exception as e:
            await self.async_session.rollback()
            raise e

        # Fetch the updated user
        select_stmt = sqlalchemy.select(User).where(User.id == user_id)
        result = await self.async_session.execute(select_stmt)
        updated_user = result.scalar()

        if not updated_user:
            raise EntityDoesNotExist(f"User with id {user_id} does not exist!")

        self.logger.debug(f"Updated user with ID {user_id}")
        return updated_user

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
        stmt = select(User, Role). \
            select_from(user_roles). \
            join(User, User.id == user_roles.c.USER_ID). \
            join(Role, Role.id == user_roles.c.ROLE_ID). \
            where(and_(user_roles.c.USER_ID == user_id, user_roles.c.ROLE_ID == role_id))
        query = await self.async_session.execute(stmt)
        user_role = query.one_or_none()

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

        return UserRoleInRemove(username=user_role[0].username, role_name=user_role[1].name)

    async def get_roles_for_user(self, user_id: int) -> typing.Sequence[Role]:
        """Get roles for user"""
        self.logger.debug(f"Getting roles for user with ID {user_id}")

        stmt = sqlalchemy.select(user_roles.c.ROLE_ID).where(user_roles.c.USER_ID == user_id)
        result = await self.async_session.execute(stmt)
        role_ids = [row[0] for row in result]

        if not role_ids:
            self.logger.debug(f"No roles found for user with ID {user_id}")
            return []

        self.logger.debug(f"Found role IDs for user with ID {user_id}")

        # Fetch the actual Role objects using the role_ids
        roles_stmt = sqlalchemy.select(Role).where(Role.id.in_(role_ids))  # type: ignore
        roles_result = await self.async_session.execute(roles_stmt)
        roles = roles_result.scalars().all()

        self.logger.debug(f"Found roles for user with ID {user_id}")

        return roles

    async def update_user_profile_pic(self, user_id: int, profile_pic: str) -> User:
        """Update user profile picture url"""
        self.logger.debug(f"Updating user with ID {user_id}")

        select_stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.async_session.execute(statement=select_stmt)
        update_user = query.scalar()

        if not update_user:
            raise EntityDoesNotExist(f"User with id `{user_id}` does not exist!")

        self.logger.debug(f"Found user with ID {user_id}")

        stmt = sqlalchemy.update(User).where(User.id == user_id).values(profile_pic=profile_pic)

        try:
            await self.async_session.execute(stmt)
            await self.async_session.commit()
        except Exception as e:
            await self.async_session.rollback()
            raise e

        self.logger.debug(f"Updated user with ID {user_id}")

        return update_user
