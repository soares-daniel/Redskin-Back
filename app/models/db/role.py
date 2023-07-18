import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class Role(Base):
    """Role table."""
    __tablename__ = "ROLE"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True,
        autoincrement=True,
        name="ID")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=False,
        name="NAME")

    # users = sqlalchemy_relationship("User", secondary=user_roles, back_populates="roles")
    # role_event_types = sqlalchemy_relationship("RoleEventType", back_populates="role")

    __mapper_args__ = {"eager_defaults": True}
