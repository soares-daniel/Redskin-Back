import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class User(Base):
    """User table."""
    __tablename__ = "USER"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True,
        autoincrement=True,
        name="ID")
    username: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=50),
        nullable=False,
        name="USERNAME")
    first_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=50),
        nullable=True,
        name="FIRST_NAME")
    last_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=50),
        nullable=True,
        name="LAST_NAME")
    _hashed_password: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=True,
        name="HASHED_PASSWORD")
    _hash_salt: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=True,
        name="HASH_SALT")
    is_active: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(
        sqlalchemy.Boolean,
        nullable=True,
        name="IS_ACTIVE")
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        name="CREATED_AT")
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
        name="UPDATED_AT"
    )
    profile_pic_url: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=True,
        name="PROFILE_PIC_URL"
    )

    # roles = sqlalchemy_relationship("Role", secondary=user_roles, back_populates="users")

    __mapper_args__ = {"eager_defaults": True}

    @property
    def hashed_password(self) -> str:
        return self._hashed_password  # type: ignore

    def set_hashed_password(self, hashed_password: str) -> None:
        self._hashed_password = hashed_password  # type: ignore

    @property
    def hash_salt(self) -> str:
        return self._hash_salt  # type: ignore

    def set_hash_salt(self, hash_salt: str) -> None:
        self._hash_salt = hash_salt  # type: ignore
