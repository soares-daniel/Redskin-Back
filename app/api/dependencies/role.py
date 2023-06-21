from fastapi import Depends
from app.repositories.user import UserRepository
from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.repository import get_repository
from app.models.db.user import User
from app.utilities.exceptions.http.exc_403 import http_403_exc_forbidden_request


def is_user_in_role(role: str):
    async def _is_user_in_role(
            current_user: User = Depends(get_current_user),
            user_repo: UserRepository = Depends(get_repository(repo_type=UserRepository))
    ) -> User:
        db_user = await user_repo.get_user_by_id(current_user.id)
        if role not in db_user.roles:
            raise http_403_exc_forbidden_request()
        return current_user
    return _is_user_in_role
