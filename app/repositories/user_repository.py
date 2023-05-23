from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from app.models.user import User


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User repository"""
    model_type = User
