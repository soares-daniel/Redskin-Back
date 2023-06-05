import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class Permission(Base):
    """Permission table."""
    __tablename__ = "PERMISSION"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True,
        autoincrement=True,
        name="ID")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=False,
        name="NAME")

    __mapper_args__ = {"eager_defaults": True}
