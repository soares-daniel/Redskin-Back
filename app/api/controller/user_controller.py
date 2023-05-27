from typing import TYPE_CHECKING


from litestar import get
from litestar.handlers.http_handlers.decorators import post
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.contrib.repository.filters import LimitOffset

from app.repositories import UserRepository
from app.models.user import UserDTO, User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def provide_users_repo(db_session: "AsyncSession") -> UserRepository:
    return UserRepository(session=db_session)


def provide_limit_offset_pagination(
    current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False,
    ),
) -> LimitOffset:
    """Add offset/limit pagination.

    Return type consumed by `Repository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    current_page : int
        LIMIT to apply to select.
    page_size : int
        OFFSET to apply to select.
    """
    return LimitOffset(page_size, page_size * (current_page - 1))


class UserController(Controller):
    """User controller"""

    dependencies = {"users_repo": Provide(provide_users_repo)}

    @get(path="/users")
    async def get_users(self,
                        users_repo: UserRepository,
                        limit_offset: LimitOffset,
                        ) -> OffsetPagination[UserDTO]:
        """Get users"""
        results, total = await users_repo.list_and_count(limit_offset)
        return OffsetPagination[UserDTO](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path="/authors")
    async def create_author(
        self,
        authors_repo: UserRepository,
        data: User,
    ) -> UserDTO:
        """Create a new author."""
        obj = await authors_repo.add(User(**data.dict(exclude_unset=True, by_alias=False, exclude_none=True)))
        await authors_repo.session.commit()
        return UserDTO.from_orm(obj)
