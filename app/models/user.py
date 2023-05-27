from sqlalchemy.orm import Mapped, mapped_column

from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto.factory import dto_field


class User(BigIntAuditBase):
    username: Mapped[str]
    password: Mapped[str] = mapped_column(info=dto_field("private"))


UserDTO = SQLAlchemyDTO[User]
