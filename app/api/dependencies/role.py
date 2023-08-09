from fastapi import Depends
from app.repositories.user import UserRepository
from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.repository import get_repository
from app.models.db.user import User
from app.utilities.exceptions.database import EntityDoesNotExist
from app.utilities.exceptions.http.exc_403 import http_403_exc_missing_role


def is_user_in_role(role: str):
    async def _is_user_in_role(
            current_user: User = Depends(get_current_user),
            user_repo: UserRepository = Depends(get_repository(repo_type=UserRepository))
    ) -> User:
        try:
            roles = await user_repo.get_roles_for_user(user_id=current_user.id)
        except EntityDoesNotExist:
            raise await http_403_exc_missing_role()

        for entry in roles:
            if entry.name == role:
                return current_user
        raise await http_403_exc_missing_role()
    return _is_user_in_role
